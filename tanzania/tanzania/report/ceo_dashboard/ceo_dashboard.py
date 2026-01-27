# Copyright (c) 2026, Nelson Mpanju and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, add_months, getdate, nowdate
from tanzania.tanzania.report.payroll_cost_analysis.payroll_cost_analysis import get_data as get_payroll_cost
from tanzania.tanzania.report.statutory_payment_tracking.statutory_payment_tracking import get_data as get_statutory_tracking
from tanzania.tanzania.report.statutory_payment_tracking.statutory_payment_tracking import calc_payroll_amounts

def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data)
	report_summary = get_report_summary(data)

	return columns, data, None, chart, report_summary

def get_columns():
	return [
		{
			"fieldname": "metric",
			"label": _("Metric"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "value",
			"label": _("Value"),
			"fieldtype": "Data", # Mixed (Currency/Count)
			"width": 150
		},
		{
			"fieldname": "trend",
			"label": _("Trend"),
			"fieldtype": "Data",
			"width": 120
		}
	]

def get_data(filters):
	company = filters.get("company")
	
	# Current Month
	today = getdate(nowdate())
	month_start = today.replace(day=1)
	
	# 1. Total Headcount
	headcount = frappe.db.count("Employee", {"status": "Active", "company": company})
	
	# 2. Current Month Payroll Cost
	# Re-use logic from payroll cost analysis if possible, but simpler
	# Just sum Salary Slip Total Cost for this month
	current_payroll_result = frappe.db.sql("""
		SELECT SUM(gross_pay) as total
		FROM `tabSalary Slip`
		WHERE company = %s AND start_date >= %s AND docstatus = 1
	""", (company, month_start), as_dict=1)
	current_payroll = flt(current_payroll_result[0].total) if current_payroll_result else 0.0
	
	# Estimate Employer Cost (approx 14%) for speed if strict not needed, OR run strict query
	# Let's run strict query for accuracy
	stat_cost = frappe.db.sql("""
		SELECT SUM(amount) FROM `tabSalary Detail` sd
		JOIN `tabSalary Slip` ss ON sd.parent = ss.name
		WHERE ss.company = %s AND ss.start_date >= %s AND ss.docstatus = 1
		AND sd.parentfield = 'earnings'
		AND sd.salary_component IN ('NSSF Expense', 'PSSF Expense', 'SDL Expense', 'WCF Expense')
	""", (company, month_start))
	
	total_monthly_cost = flt(current_payroll) + flt(stat_cost[0][0] if stat_cost else 0)

	# 3. Statutory Liabilities Outstanding
	# Calculate Payroll Amounts for current month
	stat_amts = calc_payroll_amounts(company, month_start, add_months(month_start, 1))
	total_liability = sum(stat_amts.values())
	
	rows = [
		{"metric": "Active Headcount", "value": headcount, "trend": "-"},
		{"metric": "Current Month Payroll Cost", "value": frappe.format(total_monthly_cost, "Currency"), "trend": "-"},
		{"metric": "Statutory Liability (This Month)", "value": frappe.format(total_liability, "Currency"), "trend": "-"}
	]
	
	return rows

def get_chart_data(data):
	# Trend Chart: Last 6 Months Payroll Cost
	pass # Simplified for dashboard table view for now
	
	return None

def get_report_summary(data):
	if not data:
		return []
		
	return [
		{"value": data[0]["value"], "label": "Headcount", "datatype": "Int"},
		{"value": data[1]["value"], "label": "Payroll Cost", "datatype": "Currency"},
	]
