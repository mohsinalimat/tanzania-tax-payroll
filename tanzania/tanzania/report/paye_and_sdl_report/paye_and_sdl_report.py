# Copyright (c) 2024, Navari Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate


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
			"fieldname": "department",
			"label": _("Department"),
			"fieldtype": "Link",
			"options": "Department",
			"width": 150
		},
		{
			"fieldname": "designation",
			"label": _("Designation"),
			"fieldtype": "Link",
			"options": "Designation",
			"width": 150
		},
		{
			"fieldname": "gross_pay",
			"label": _("Gross Pay"),
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"fieldname": "nssf_employee",
			"label": _("NSSF Employee"),
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"fieldname": "taxable_income",
			"label": _("Taxable Income"),
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"fieldname": "paye_0",
			"label": _("PAYE 0%"),
			"fieldtype": "Currency",
			"width": 110
		},
		{
			"fieldname": "paye_8",
			"label": _("PAYE 8%"),
			"fieldtype": "Currency",
			"width": 110
		},
		{
			"fieldname": "paye_20",
			"label": _("PAYE 20%"),
			"fieldtype": "Currency",
			"width": 110
		},
		{
			"fieldname": "paye_25",
			"label": _("PAYE 25%"),
			"fieldtype": "Currency",
			"width": 110
		},
		{
			"fieldname": "paye_30",
			"label": _("PAYE 30%"),
			"fieldtype": "Currency",
			"width": 110
		},
		{
			"fieldname": "total_paye",
			"label": _("Total PAYE"),
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"fieldname": "sdl",
			"label": _("SDL (3.5%)"),
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"fieldname": "net_pay",
			"label": _("Net Pay"),
			"fieldtype": "Currency",
			"width": 130
		}
	]


def get_data(filters):
	"""Get salary slip data and calculate PAYE by bracket and SDL"""
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
		ORDER BY ss.employee, ss.posting_date
	""", filters, as_dict=1)

	data = []

	for slip in salary_slips:
		# Get NSSF employee contribution
		nssf_employee = get_component_amount(slip.name, "NSSF")

		# Get PAYE amount
		paye_total = get_component_amount(slip.name, "PAYE")

		# Calculate taxable income (gross - NSSF employee contribution)
		taxable_income = flt(slip.gross_pay) - flt(nssf_employee)

		# Calculate PAYE by bracket
		paye_breakdown = calculate_paye_by_bracket(taxable_income)

		# Calculate SDL (3.5% of gross pay - employer contribution)
		sdl_amount = flt(slip.gross_pay) * 0.035

		row = {
			"employee": slip.employee,
			"employee_name": slip.employee_name,
			"department": slip.department,
			"designation": slip.designation,
			"gross_pay": flt(slip.gross_pay),
			"nssf_employee": flt(nssf_employee),
			"taxable_income": flt(taxable_income),
			"paye_0": flt(paye_breakdown.get("paye_0", 0)),
			"paye_8": flt(paye_breakdown.get("paye_8", 0)),
			"paye_20": flt(paye_breakdown.get("paye_20", 0)),
			"paye_25": flt(paye_breakdown.get("paye_25", 0)),
			"paye_30": flt(paye_breakdown.get("paye_30", 0)),
			"total_paye": flt(paye_total),
			"sdl": flt(sdl_amount),
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


def calculate_paye_by_bracket(taxable_income):
	"""
	Calculate PAYE by tax bracket for Tanzania

	Tax Brackets (Monthly):
	- 0%: First 270,000 TZS
	- 8%: 270,001 to 520,000 TZS
	- 20%: 520,001 to 760,000 TZS
	- 25%: 760,001 to 1,000,000 TZS
	- 30%: Above 1,000,000 TZS
	"""
	taxable_income = flt(taxable_income)

	paye_breakdown = {
		"paye_0": 0,
		"paye_8": 0,
		"paye_20": 0,
		"paye_25": 0,
		"paye_30": 0
	}

	if taxable_income <= 0:
		return paye_breakdown

	# Bracket thresholds
	bracket_1 = 270000  # 0%
	bracket_2 = 520000  # 8%
	bracket_3 = 760000  # 20%
	bracket_4 = 1000000  # 25%
	# Above bracket_4 = 30%

	remaining_income = taxable_income

	# 0% bracket (first 270,000)
	if remaining_income > 0:
		amount_in_bracket = min(remaining_income, bracket_1)
		paye_breakdown["paye_0"] = 0  # No tax in this bracket
		remaining_income -= amount_in_bracket

	# 8% bracket (270,001 to 520,000)
	if remaining_income > 0:
		amount_in_bracket = min(remaining_income, bracket_2 - bracket_1)
		paye_breakdown["paye_8"] = amount_in_bracket * 0.08
		remaining_income -= amount_in_bracket

	# 20% bracket (520,001 to 760,000)
	if remaining_income > 0:
		amount_in_bracket = min(remaining_income, bracket_3 - bracket_2)
		paye_breakdown["paye_20"] = amount_in_bracket * 0.20
		remaining_income -= amount_in_bracket

	# 25% bracket (760,001 to 1,000,000)
	if remaining_income > 0:
		amount_in_bracket = min(remaining_income, bracket_4 - bracket_3)
		paye_breakdown["paye_25"] = amount_in_bracket * 0.25
		remaining_income -= amount_in_bracket

	# 30% bracket (above 1,000,000)
	if remaining_income > 0:
		paye_breakdown["paye_30"] = remaining_income * 0.30

	return paye_breakdown
