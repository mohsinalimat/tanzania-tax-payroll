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
	"""Return columns for PAYE & SDL Report"""
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
			"width": 180
		},
		{
			"fieldname": "gross_pay",
			"label": _("Gross Pay"),
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "nssf_employee",
			"label": _("NSSF (Employee)"),
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "taxable_income",
			"label": _("Taxable Income"),
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "paye",
			"label": _("PAYE"),
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "sdl",
			"label": _("SDL (3.5%)"),
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
			"fieldname": "wcf",
			"label": _("WCF (1%)"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "net_pay",
			"label": _("Net Pay"),
			"fieldtype": "Currency",
			"width": 140
		}
	]


def get_data(filters):
	"""Get salary slip data for PAYE and SDL report"""
	if not filters:
		filters = {}

	conditions = get_conditions(filters)

	salary_slips = frappe.db.sql(f"""
		SELECT
			ss.name,
			ss.employee,
			ss.employee_name,
			ss.department,
			ss.designation,
			ss.gross_pay,
			ss.net_pay,
			ss.posting_date
		FROM `tabSalary Slip` ss
		WHERE ss.docstatus = 1
			{conditions}
		ORDER BY ss.employee_name, ss.posting_date
	""", filters, as_dict=1)

	data = []

	for slip in salary_slips:
		# Get NSSF employee contribution (deduction)
		nssf_employee = get_deduction_amount(slip.name, ["NSSF", "NSSF Employee"])

		# Get PAYE amount (deduction)
		paye = get_deduction_amount(slip.name, ["PAYE", "Income Tax", "Pay As You Earn"])

		# Get employer contributions from salary slip
		nssf_employer = get_earning_amount(slip.name, ["NSSF Employer", "NSSF - Employer"])
		sdl = get_earning_amount(slip.name, ["SDL", "Skills Development Levy"])
		wcf = get_earning_amount(slip.name, ["WCF", "Workers Compensation Fund"])

		# Calculate taxable income (gross - NSSF employee contribution)
		taxable_income = flt(slip.gross_pay) - flt(nssf_employee)

		# If SDL not found in salary slip, calculate it (3.5% of gross)
		if not sdl:
			sdl = flt(slip.gross_pay) * 0.035

		# If WCF not found, calculate it (1% of gross)
		if not wcf:
			wcf = flt(slip.gross_pay) * 0.01

		# If NSSF employer not found, assume same as employee (10% each)
		if not nssf_employer:
			nssf_employer = flt(nssf_employee)

		row = {
			"employee": slip.employee,
			"employee_name": slip.employee_name,
			"gross_pay": flt(slip.gross_pay),
			"nssf_employee": flt(nssf_employee),
			"taxable_income": flt(taxable_income),
			"paye": flt(paye),
			"sdl": flt(sdl),
			"nssf_employer": flt(nssf_employer),
			"wcf": flt(wcf),
			"net_pay": flt(slip.net_pay)
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


def get_deduction_amount(salary_slip, component_names):
	"""Get the amount for a deduction component (searches multiple possible names)"""
	for name in component_names:
		amount = frappe.db.get_value(
			"Salary Detail",
			{
				"parent": salary_slip,
				"parenttype": "Salary Slip",
				"salary_component": ["like", f"%{name}%"],
				"parentfield": "deductions"
			},
			"amount"
		)
		if amount:
			return flt(amount)

	# Also try exact match
	for name in component_names:
		amount = frappe.db.get_value(
			"Salary Detail",
			{
				"parent": salary_slip,
				"parenttype": "Salary Slip",
				"salary_component": name,
				"parentfield": "deductions"
			},
			"amount"
		)
		if amount:
			return flt(amount)

	return 0


def get_earning_amount(salary_slip, component_names):
	"""Get the amount for an earning/employer component"""
	for name in component_names:
		amount = frappe.db.get_value(
			"Salary Detail",
			{
				"parent": salary_slip,
				"parenttype": "Salary Slip",
				"salary_component": ["like", f"%{name}%"]
			},
			"amount"
		)
		if amount:
			return flt(amount)

	return 0
