# Copyright (c) 2024, Navari Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, get_first_day, get_last_day

# Map Statutory Types to Suppliers and Salary Components
# NOTE: Only include components that create actual PAYABLES (Deductions), 
# NOT statistical Expense components (Earnings with do_not_include_in_total).
# Per payroll_setup.py:
# - "NSSF" (employee 10%) + "NSSF Employer" (employer 10%) = Total 20% posted to NSSF Payable
# - "PSSF" (employee 5%) + "PSSF Employer" (employer 15%) = Total 20% posted to NSSF Payable
# - "SDL" (deduction) = 3.5% posted to SDL Payable
# - "WCF" (deduction) = 0.5% posted to WCF Payable (employer only)
# - "PAYE- (Tax)" = Posted to PAYE Payable
# - "HESLB" = Posted to HESLB Payable

STATUTORY_MAP = {
	"PAYE": {
		"supplier": "Tanzania Revenue Authority (TRA)",
		"components": ["PAYE- (Tax)"],  # The actual PAYE deduction component
		"due_date_offset": 7  # 7th of next month
	},
	"SDL": {
		"supplier": "Tanzania Revenue Authority (TRA)",
		"components": ["SDL"],  # Deduction component only (not SDL Expense which is statistical)
		"due_date_offset": 7
	},
	"NSSF": {
		"supplier": "National Social Security Fund (NSSF)", 
		"components": ["NSSF", "NSSF Employer"],  # Employee + Employer deductions = 20% total
		"due_date_offset": 30
	},
	"PSSF": {
		"supplier": "Public Service Social Security Fund (PSSF)",
		"components": ["PSSF", "PSSF Employer"],  # Employee (5%) + Employer (15%) = 20% total
		"due_date_offset": 30
	},
	"WCF": {
		"supplier": "Workers Compensation Fund (WCF)",
		"components": ["WCF"],  # Deduction component only (not WCF Expense which is statistical)
		"due_date_offset": 30
	},
	"HESLB": {
		"supplier": "Higher Education Students Loans Board (HESLB)",
		"components": ["HESLB"],
		"due_date_offset": 30
	}
}

def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data)

	return columns, data, None, chart

def get_columns():
	return [
		{
			"fieldname": "statutory_type",
			"label": _("Statutory Type"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "supplier",
			"label": _("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 200
		},
		{
			"fieldname": "amount_due",
			"label": _("Amount Due (Payroll)"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "amount_paid",
			"label": _("Amount Paid"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "balance",
			"label": _("Balance / Outstanding"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 120
		}
	]

def get_data(filters):
	period = filters.get("period")
	company = filters.get("company")
	
	if not period:
		return []

	# Define Month Range
	start_date = get_first_day(period)
	end_date = get_last_day(period)
	
	# 1. Calculate Amount Due from Salary Slips
	# We sum relevant components from Salary Detail
	payroll_amounts = calc_payroll_amounts(company, start_date, end_date)

	# 2. Calculate Amount Paid from Payments/GL
	# We look for Payments to the Supplier in the relevant window
	# Usually payment is made NEXT month, but we check matching period
	# For simplicity, we check payments posted in the Date Range + 30 days buffer
	# OR we check GL Entries against the Supplier where Account is Payable
	payment_amounts = calc_payment_amounts(company, start_date, end_date)

	data = []
	for stat_type, config in STATUTORY_MAP.items():
		due = payroll_amounts.get(stat_type, 0.0)
		paid = payment_amounts.get(config["supplier"], 0.0)
		balance = due - paid
		
		status = "Paid"
		if balance > 100: # Threshold for small diffs
			status = "Outstanding"
		elif balance < -100:
			status = "Overpaid"
			
		if due == 0 and paid == 0:
			continue

		data.append({
			"statutory_type": stat_type,
			"supplier": config["supplier"],
			"amount_due": due,
			"amount_paid": paid,
			"balance": balance,
			"status": status
		})
		
	return data

def calc_payroll_amounts(company, start_date, end_date):
	amounts = {}
	
	# Fetch Salary Slips in this month
	salary_slips = frappe.get_all("Salary Slip", 
		filters={
			"company": company,
			"docstatus": 1,
			"start_date": [">=", start_date],
			"end_date": ["<=", end_date]
		},
		pluck="name"
	)
	
	if not salary_slips:
		return amounts

	# Aggregated query for efficiency
	# We need to map component -> statutory type
	comp_map = {}
	all_comps = []
	for st_type, conf in STATUTORY_MAP.items():
		for c in conf["components"]:
			comp_map[c] = st_type
			all_comps.append(c)
			
	details = frappe.db.sql("""
		SELECT salary_component, SUM(amount) as total
		FROM `tabSalary Detail`
		WHERE 
			parent IN %(slips)s
			AND salary_component IN %(comps)s
		GROUP BY salary_component
	""", {"slips": salary_slips, "comps": all_comps}, as_dict=1)
	
	for d in details:
		st_type = comp_map.get(d.salary_component)
		if st_type:
			amounts[st_type] = amounts.get(st_type, 0.0) + flt(d.total)
			
	return amounts

def calc_payment_amounts(company, start_date, end_date):
	# Calculate payments made to Statutory Suppliers
	# We search for Payment Entries or Journal Entries where Party is Supplier
	# Filter: Posting Date typically in the NEXT month (since due date is 7th/30th of next month)
	# So we search current Period Start -> Period End + 45 days
	
	import datetime
	
	check_start = start_date
	# Add ~45 days to end_date to capture next month payments
	check_end = frappe.utils.add_days(end_date, 45)
	
	suppliers = [conf["supplier"] for conf in STATUTORY_MAP.values()]
	
	# Using GL Entry is most reliable for "Paid Amount"
	# We check Debit amounts against Payable account for these suppliers
	# Or just check "Dr" amount for Party Type Supplier
	
	gl_entries = frappe.db.sql("""
		SELECT party, SUM(debit) as paid
		FROM `tabGL Entry`
		WHERE 
			company = %(company)s
			AND party_type = 'Supplier'
			AND party IN %(suppliers)s
			AND posting_date BETWEEN %(start)s AND %(end)s
			AND is_cancelled = 0
		GROUP BY party
	""", {
		"company": company, 
		"suppliers": suppliers,
		"start": check_start,
		"end": check_end
	}, as_dict=1)
	
	result = {}
	for gle in gl_entries:
		result[gle.party] = flt(gle.paid)
		
	return result

def get_chart_data(data):
	if not data:
		return None
		
	labels = [d.get("statutory_type") for d in data]
	due = [d.get("amount_due") for d in data]
	paid = [d.get("amount_paid") for d in data]
	
	return {
		"data": {
			"labels": labels,
			"datasets": [
				{"name": _("Due"), "values": due},
				{"name": _("Paid"), "values": paid}
			]
		},
		"type": "bar",
		"colors": ["#ff4d4d", "#00cc66"]
	}
