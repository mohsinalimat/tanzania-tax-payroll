# Copyright (c) 2024, Navari Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	"""Return columns for NSSF Contribution Report"""
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
			"fieldname": "date_of_joining",
			"label": _("Date of Joining"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "department",
			"label": _("Department"),
			"fieldtype": "Link",
			"options": "Department",
			"width": 150
		},
		{
			"fieldname": "gross_pay",
			"label": _("Gross Pay"),
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"fieldname": "employee_contribution",
			"label": _("Employee Contribution (10%)"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "employer_contribution",
			"label": _("Employer Contribution (10%)"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "total_contribution",
			"label": _("Total Contribution (20%)"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "running_total",
			"label": _("Running Total"),
			"fieldtype": "Currency",
			"width": 150
		}
	]


def get_data(filters):
	"""Get NSSF contribution data for all NSSF-registered employees"""
	if not filters:
		filters = {}

	conditions = get_conditions(filters)

	# Get salary slip data for employees registered for NSSF
	salary_slips = frappe.db.sql(f"""
		SELECT
			ss.name,
			ss.employee,
			ss.employee_name,
			ss.department,
			ss.gross_pay,
			ss.posting_date,
			e.date_of_joining,
			e.nssf
		FROM `tabSalary Slip` ss
		INNER JOIN `tabEmployee` e ON ss.employee = e.name
		WHERE ss.docstatus = 1
			AND e.nssf = 1
			{conditions}
		ORDER BY ss.employee, ss.posting_date
	""", filters, as_dict=1)

	data = []
	running_total = 0

	for slip in salary_slips:
		# Get NSSF employee contribution from salary slip
		employee_contribution = get_component_amount(slip.name, "NSSF")

		# Calculate employer contribution (10% of gross pay)
		employer_contribution = flt(slip.gross_pay) * 0.10

		# Total contribution
		total_contribution = flt(employee_contribution) + flt(employer_contribution)

		# Update running total
		running_total += total_contribution

		row = {
			"employee": slip.employee,
			"employee_name": slip.employee_name,
			"date_of_joining": slip.date_of_joining,
			"department": slip.department,
			"gross_pay": flt(slip.gross_pay),
			"employee_contribution": flt(employee_contribution),
			"employer_contribution": flt(employer_contribution),
			"total_contribution": flt(total_contribution),
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


def get_component_amount(salary_slip, component_name):
	"""Get the amount for a specific salary component from salary slip"""
	amount = frappe.db.get_value(
		"Salary Detail",
		{
			"parent": salary_slip,
			"parenttype": "Salary Slip",
			"salary_component": component_name
		},
		"amount"
	)
	return flt(amount)
