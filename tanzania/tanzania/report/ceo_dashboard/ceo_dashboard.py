# Copyright (c) 2026, Nelson Mpanju and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(filters)
	report_summary = get_report_summary(data)

	return columns, data, None, chart, report_summary


def get_columns():
	return [
		{
			"fieldname": "metric",
			"label": _("Metric"),
			"fieldtype": "Data",
			"width": 250
		},
		{
			"fieldname": "value",
			"label": _("Value"),
			"fieldtype": "Currency",
			"width": 180
		}
	]


def get_data(filters):
	company = filters.get("company")
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	# 1. Total Headcount
	headcount = frappe.db.count("Employee", {"status": "Active", "company": company})

	# 2. Payroll Cost (Gross Pay)
	gross_pay_result = frappe.db.sql("""
		SELECT SUM(gross_pay) as total
		FROM `tabSalary Slip`
		WHERE company = %s
			AND start_date >= %s
			AND end_date <= %s
			AND docstatus = 1
	""", (company, from_date, to_date), as_dict=1)
	gross_pay = flt(gross_pay_result[0].total) if gross_pay_result else 0.0

	# 3. PAYE Total
	paye_result = frappe.db.sql("""
		SELECT SUM(sd.amount) as total
		FROM `tabSalary Detail` sd
		JOIN `tabSalary Slip` ss ON sd.parent = ss.name
		WHERE ss.company = %s
			AND ss.start_date >= %s
			AND ss.end_date <= %s
			AND ss.docstatus = 1
			AND sd.parentfield = 'deductions'
			AND sd.salary_component LIKE '%%PAYE%%'
	""", (company, from_date, to_date), as_dict=1)
	paye_total = flt(paye_result[0].total) if paye_result else 0.0

	# 4. NSSF Employee Contribution
	nssf_emp_result = frappe.db.sql("""
		SELECT SUM(sd.amount) as total
		FROM `tabSalary Detail` sd
		JOIN `tabSalary Slip` ss ON sd.parent = ss.name
		WHERE ss.company = %s
			AND ss.start_date >= %s
			AND ss.end_date <= %s
			AND ss.docstatus = 1
			AND sd.parentfield = 'deductions'
			AND sd.salary_component LIKE '%%NSSF%%'
	""", (company, from_date, to_date), as_dict=1)
	nssf_employee = flt(nssf_emp_result[0].total) if nssf_emp_result else 0.0

	# 5. SDL (3.5% of Gross)
	sdl_total = flt(gross_pay) * 0.035

	# 6. WCF (1% of Gross)
	wcf_total = flt(gross_pay) * 0.01

	# 7. NSSF Employer (same as employee - 10%)
	nssf_employer = flt(nssf_employee)

	# 8. Total Statutory Liability
	total_statutory = paye_total + nssf_employee + nssf_employer + sdl_total + wcf_total

	# 9. Net Pay
	net_pay_result = frappe.db.sql("""
		SELECT SUM(net_pay) as total
		FROM `tabSalary Slip`
		WHERE company = %s
			AND start_date >= %s
			AND end_date <= %s
			AND docstatus = 1
	""", (company, from_date, to_date), as_dict=1)
	net_pay = flt(net_pay_result[0].total) if net_pay_result else 0.0

	rows = [
		{"metric": "Active Headcount", "value": headcount},
		{"metric": "Gross Payroll", "value": gross_pay},
		{"metric": "PAYE (Income Tax)", "value": paye_total},
		{"metric": "NSSF - Employee (10%)", "value": nssf_employee},
		{"metric": "NSSF - Employer (10%)", "value": nssf_employer},
		{"metric": "SDL (3.5%)", "value": sdl_total},
		{"metric": "WCF (1%)", "value": wcf_total},
		{"metric": "Total Statutory Liability", "value": total_statutory},
		{"metric": "Net Pay to Employees", "value": net_pay},
	]

	return rows


def get_chart_data(filters):
	"""Generate chart showing payroll breakdown"""
	company = filters.get("company")
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	# Get gross pay
	gross_result = frappe.db.sql("""
		SELECT SUM(gross_pay) as total
		FROM `tabSalary Slip`
		WHERE company = %s AND start_date >= %s AND end_date <= %s AND docstatus = 1
	""", (company, from_date, to_date), as_dict=1)
	gross_pay = flt(gross_result[0].total) if gross_result else 0.0

	# Get PAYE
	paye_result = frappe.db.sql("""
		SELECT SUM(sd.amount) as total
		FROM `tabSalary Detail` sd
		JOIN `tabSalary Slip` ss ON sd.parent = ss.name
		WHERE ss.company = %s AND ss.start_date >= %s AND ss.end_date <= %s AND ss.docstatus = 1
			AND sd.parentfield = 'deductions' AND sd.salary_component LIKE '%%PAYE%%'
	""", (company, from_date, to_date), as_dict=1)
	paye = flt(paye_result[0].total) if paye_result else 0.0

	# Get NSSF
	nssf_result = frappe.db.sql("""
		SELECT SUM(sd.amount) as total
		FROM `tabSalary Detail` sd
		JOIN `tabSalary Slip` ss ON sd.parent = ss.name
		WHERE ss.company = %s AND ss.start_date >= %s AND ss.end_date <= %s AND ss.docstatus = 1
			AND sd.parentfield = 'deductions' AND sd.salary_component LIKE '%%NSSF%%'
	""", (company, from_date, to_date), as_dict=1)
	nssf = flt(nssf_result[0].total) if nssf_result else 0.0

	sdl = gross_pay * 0.035
	wcf = gross_pay * 0.01

	# Get net pay
	net_result = frappe.db.sql("""
		SELECT SUM(net_pay) as total
		FROM `tabSalary Slip`
		WHERE company = %s AND start_date >= %s AND end_date <= %s AND docstatus = 1
	""", (company, from_date, to_date), as_dict=1)
	net_pay = flt(net_result[0].total) if net_result else 0.0

	return {
		"data": {
			"labels": ["Net Pay", "PAYE", "NSSF (Emp+Empr)", "SDL", "WCF"],
			"datasets": [
				{
					"name": "Amount",
					"values": [net_pay, paye, nssf * 2, sdl, wcf]
				}
			]
		},
		"type": "bar",
		"colors": ["#28a745", "#dc3545", "#007bff", "#ffc107", "#17a2b8"]
	}


def get_report_summary(data):
	if not data:
		return []

	return [
		{"value": data[0]["value"], "label": "Headcount", "datatype": "Int", "indicator": "blue"},
		{"value": data[1]["value"], "label": "Gross Payroll", "datatype": "Currency", "indicator": "green"},
		{"value": data[7]["value"], "label": "Total Statutory", "datatype": "Currency", "indicator": "red"},
		{"value": data[8]["value"], "label": "Net Pay", "datatype": "Currency", "indicator": "green"},
	]
