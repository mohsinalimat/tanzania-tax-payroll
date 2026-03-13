# Copyright (c) 2026, Nelson Mpanju and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, formatdate


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns()
	data = get_data(filters)
	chart_data = get_chart_data(data)

	return columns, data, None, chart_data


def get_columns():
	"""Return columns for Monthly Payroll Summary"""
	return [
		{
			"fieldname": "department",
			"label": _("Department"),
			"fieldtype": "Link",
			"options": "Department",
			"width": 180
		},
		{
			"fieldname": "employee_count",
			"label": _("Headcount"),
			"fieldtype": "Int",
			"width": 100
		},
		{
			"fieldname": "gross_pay",
			"label": _("Gross Pay"),
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "basic_salary",
			"label": _("Basic Salary"),
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "allowances",
			"label": _("Allowances"),
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"fieldname": "nssf_employee",
			"label": _("NSSF (Employee)"),
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "nssf_employer",
			"label": _("NSSF (Employer)"),
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "paye",
			"label": _("PAYE"),
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"fieldname": "sdl",
			"label": _("SDL"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "wcf",
			"label": _("WCF"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "heslb",
			"label": _("HESLB"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "other_deductions",
			"label": _("Other Deductions"),
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "total_deductions",
			"label": _("Total Deductions"),
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "net_pay",
			"label": _("Net Pay"),
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "total_cost",
			"label": _("Total Cost to Company"),
			"fieldtype": "Currency",
			"width": 160
		}
	]


def get_data(filters):
	"""Get monthly payroll summary data grouped by department"""
	conditions = get_conditions(filters)

	# Get salary slip data
	salary_slips = frappe.db.sql("""
		SELECT
			ss.name,
			ss.department,
			ss.employee,
			ss.gross_pay,
			ss.total_deduction,
			ss.net_pay
		FROM `tabSalary Slip` ss
		WHERE ss.docstatus = 1
	""" + conditions, filters, as_dict=1)

	# Group data by department
	department_data = {}

	for slip in salary_slips:
		dept = slip.department or "Unassigned"

		if dept not in department_data:
			department_data[dept] = {
				"department": dept,
				"employee_count": 0,
				"employees": set(),
				"gross_pay": 0,
				"basic_salary": 0,
				"allowances": 0,
				"nssf_employee": 0,
				"nssf_employer": 0,
				"paye": 0,
				"sdl": 0,
				"wcf": 0,
				"heslb": 0,
				"other_deductions": 0,
				"total_deductions": 0,
				"net_pay": 0,
				"total_cost": 0
			}

		# Track unique employees
		department_data[dept]["employees"].add(slip.employee)

		# Aggregate gross pay, deductions, net pay
		department_data[dept]["gross_pay"] += flt(slip.gross_pay)
		department_data[dept]["total_deductions"] += flt(slip.total_deduction)
		department_data[dept]["net_pay"] += flt(slip.net_pay)

		# Get component-wise breakdown
		components = get_salary_components(slip.name)

		department_data[dept]["basic_salary"] += flt(components.get("basic_salary", 0))
		department_data[dept]["allowances"] += flt(components.get("allowances", 0))
		department_data[dept]["nssf_employee"] += flt(components.get("nssf_employee", 0))
		department_data[dept]["paye"] += flt(components.get("paye", 0))
		department_data[dept]["heslb"] += flt(components.get("heslb", 0))
		department_data[dept]["other_deductions"] += flt(components.get("other_deductions", 0))

		# Calculate employer contributions
		department_data[dept]["nssf_employer"] += flt(slip.gross_pay) * 0.10
		department_data[dept]["sdl"] += flt(slip.gross_pay) * 0.035
		department_data[dept]["wcf"] += flt(slip.gross_pay) * 0.005

	# Convert to list and calculate totals
	data = []
	for dept, values in department_data.items():
		# Employee count is the number of unique employees
		values["employee_count"] = len(values["employees"])
		del values["employees"]  # Remove the set before returning

		# Calculate total cost to company (gross + employer contributions)
		values["total_cost"] = (
			flt(values["gross_pay"]) +
			flt(values["nssf_employer"]) +
			flt(values["sdl"]) +
			flt(values["wcf"])
		)

		data.append(values)

	# Sort by department
	data = sorted(data, key=lambda x: x["department"])

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

	if filters.get("department"):
		conditions += " AND ss.department = %(department)s"

	return conditions


def get_salary_components(salary_slip):
	"""Get breakdown of salary components for a slip"""
	components = {
		"basic_salary": 0,
		"allowances": 0,
		"nssf_employee": 0,
		"paye": 0,
		"heslb": 0,
		"other_deductions": 0
	}

	# Get all salary details for this slip
	salary_details = frappe.db.sql("""
		SELECT
			salary_component,
			amount,
			parentfield
		FROM `tabSalary Detail`
		WHERE parent = %s
			AND parenttype = 'Salary Slip'
	""", salary_slip, as_dict=1)

	for detail in salary_details:
		component = detail.salary_component
		amount = flt(detail.amount)

		if detail.parentfield == "earnings":
			# Earnings
			if component == "Basic":
				components["basic_salary"] += amount
			else:
				components["allowances"] += amount

		elif detail.parentfield == "deductions":
			# Deductions
			if component == "NSSF":
				components["nssf_employee"] += amount
			elif component == "PAYE":
				components["paye"] += amount
			elif component == "HESLB":
				components["heslb"] += amount
			else:
				components["other_deductions"] += amount

	return components


def get_chart_data(data):
	"""Generate chart data for visualization"""
	if not data:
		return None

	departments = [row["department"] for row in data]
	gross_pay_values = [row["gross_pay"] for row in data]
	net_pay_values = [row["net_pay"] for row in data]
	total_cost_values = [row["total_cost"] for row in data]

	chart = {
		"data": {
			"labels": departments,
			"datasets": [
				{
					"name": "Gross Pay",
					"values": gross_pay_values
				},
				{
					"name": "Net Pay",
					"values": net_pay_values
				},
				{
					"name": "Total Cost",
					"values": total_cost_values
				}
			]
		},
		"type": "bar",
		"colors": ["#4CAF50", "#2196F3", "#FF9800"]
	}

	return chart
