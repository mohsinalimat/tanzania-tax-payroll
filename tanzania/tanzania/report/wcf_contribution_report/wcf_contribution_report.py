# Copyright (c) 2026, Nelson Mpanju and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	"""Return columns for WCF Contribution Report"""
	return [
		{
			"fieldname": "employee",
			"label": _("Employee ID"),
			"fieldtype": "Link",
			"options": "Employee",
			"width": 120
		},
		{
			"fieldname": "employee_name",
			"label": _("Employee Name"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "wcf_number",
			"label": _("WCF Number"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "designation",
			"label": _("Designation"),
			"fieldtype": "Link",
			"options": "Designation",
			"width": 150
		},
		{
			"fieldname": "department",
			"label": _("Department"),
			"fieldtype": "Link",
			"options": "Department",
			"width": 150
		},
		{
			"fieldname": "date_of_joining",
			"label": _("Date of Joining"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "gross_pay",
			"label": _("Gross Pay"),
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"fieldname": "wcf_contribution",
			"label": _("WCF Contribution (0.5%)"),
			"fieldtype": "Currency",
			"width": 160
		},
		{
			"fieldname": "running_total",
			"label": _("Running Total"),
			"fieldtype": "Currency",
			"width": 150
		}
	]


def get_data(filters):
	"""Get WCF contribution data for all employees (employer-only contribution)"""
	if not filters:
		filters = {}

	conditions = get_conditions(filters)

	# Get salary slip data for all employees
	salary_slips = frappe.db.sql("""
		SELECT
			ss.name,
			ss.employee,
			ss.employee_name,
			ss.department,
			ss.designation,
			ss.gross_pay,
			ss.posting_date,
			e.date_of_joining,
			e.wcf_number
		FROM `tabSalary Slip` ss
		INNER JOIN `tabEmployee` e ON ss.employee = e.name
		WHERE ss.docstatus = 1
	""" + conditions + """
		ORDER BY ss.employee, ss.posting_date
	""", filters, as_dict=1)

	data = []
	running_total = 0

	for slip in salary_slips:
		# Calculate WCF contribution (0.5% of gross pay - employer only)
		wcf_contribution = flt(slip.gross_pay) * 0.005

		# Update running total
		running_total += wcf_contribution

		row = {
			"employee": slip.employee,
			"employee_name": slip.employee_name,
			"wcf_number": slip.wcf_number or "",
			"designation": slip.designation,
			"department": slip.department,
			"date_of_joining": slip.date_of_joining,
			"gross_pay": flt(slip.gross_pay),
			"wcf_contribution": flt(wcf_contribution),
			"running_total": flt(running_total)
		}

		data.append(row)

	return data


def get_conditions(filters):
	"""Build SQL conditions from filters"""
	conditions = ""

	if filters.get("company"):
		conditions += " AND ss.company = %(company)s"

	if filters.get("from_date"):
		conditions += " AND ss.start_date >= %(from_date)s"

	if filters.get("to_date"):
		conditions += " AND ss.end_date <= %(to_date)s"

	if filters.get("employee"):
		conditions += " AND ss.employee = %(employee)s"

	if filters.get("department"):
		conditions += " AND ss.department = %(department)s"

	return conditions
