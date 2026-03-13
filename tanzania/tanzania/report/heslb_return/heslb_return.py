# Copyright (c) 2026, Nelson Mpanju and contributors
# For license information, please see license.txt

"""
HESLB Return Online Report
Higher Education Students Loans Board monthly deduction report
Format for online submission to HESLB portal
"""

import frappe
from frappe import _
from frappe.utils import flt, getdate, formatdate


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	"""HESLB Return columns based on HESLB portal format"""
	return [
		{
			"fieldname": "sn",
			"label": _("S/N"),
			"fieldtype": "Int",
			"width": 50,
		},
		{
			"fieldname": "employee_id",
			"label": _("Employee ID"),
			"fieldtype": "Link",
			"options": "Employee",
			"width": 120,
		},
		{
			"fieldname": "employee_name",
			"label": _("Employee Name"),
			"fieldtype": "Data",
			"width": 180,
		},
		{
			"fieldname": "nida_no",
			"label": _("NIDA No."),
			"fieldtype": "Data",
			"width": 140,
		},
		{
			"fieldname": "loan_no",
			"label": _("HESLB Loan No."),
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"fieldname": "department",
			"label": _("Department"),
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"fieldname": "gross_salary",
			"label": _("Gross Salary (TZS)"),
			"fieldtype": "Currency",
			"width": 130,
		},
		{
			"fieldname": "deduction_rate",
			"label": _("Rate (%)"),
			"fieldtype": "Percent",
			"width": 80,
		},
		{
			"fieldname": "heslb_deduction",
			"label": _("HESLB Deduction (TZS)"),
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"fieldname": "pay_period",
			"label": _("Pay Period"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "salary_slip",
			"label": _("Salary Slip"),
			"fieldtype": "Link",
			"options": "Salary Slip",
			"width": 150,
		},
	]


def get_data(filters):
	"""Get HESLB deduction data from Salary Slips"""
	company = filters.get("company")
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	conditions = get_conditions(filters)

	# Get salary slips with HESLB deductions
	# Note: nida and heslb are custom fields on Employee
	salary_slips = frappe.db.sql("""
		SELECT
			ss.name as salary_slip,
			ss.employee,
			ss.employee_name,
			ss.department,
			ss.gross_pay as gross_salary,
			ss.posting_date,
			ss.start_date,
			ss.end_date,
			e.heslb,
			COALESCE(e.nida, '') as nida_no,
			COALESCE(e.heslb, '') as loan_no
		FROM `tabSalary Slip` ss
		INNER JOIN `tabEmployee` e ON ss.employee = e.name
		WHERE ss.docstatus = 1
			AND ss.company = %(company)s
			AND ss.posting_date BETWEEN %(from_date)s AND %(to_date)s
			AND e.heslb IS NOT NULL AND e.heslb != ''
			""" + conditions + """
		ORDER BY ss.employee, ss.posting_date
	""", {  # nosemgrep: frappe-sql-format-injection
		"company": company,
		"from_date": from_date,
		"to_date": to_date,
		"employee": filters.get("employee"),
		"department": filters.get("department"),
	}, as_dict=1)

	data = []
	sn = 0

	for slip in salary_slips:
		# Get HESLB deduction amount from salary slip
		heslb_amount = get_heslb_deduction(slip.salary_slip)

		if heslb_amount > 0:
			sn += 1
			# Calculate rate (should be 15%)
			rate = (heslb_amount / slip.gross_salary * 100) if slip.gross_salary else 15

			# Format pay period
			pay_period = ""
			if slip.start_date and slip.end_date:
				pay_period = f"{formatdate(slip.start_date, 'MMM yyyy')}"

			data.append({
				"sn": sn,
				"employee_id": slip.employee,
				"employee_name": slip.employee_name,
				"nida_no": slip.nida_no or "",
				"loan_no": slip.loan_no or "",
				"department": slip.department or "",
				"gross_salary": flt(slip.gross_salary),
				"deduction_rate": flt(rate, 2),
				"heslb_deduction": flt(heslb_amount),
				"pay_period": pay_period,
				"salary_slip": slip.salary_slip,
			})

	return data


def get_heslb_deduction(salary_slip):
	"""Get HESLB deduction amount from salary slip"""
	result = frappe.db.sql("""
		SELECT COALESCE(SUM(amount), 0) as amount
		FROM `tabSalary Detail`
		WHERE parent = %s
			AND parentfield = 'deductions'
			AND salary_component = 'HESLB'
	""", salary_slip)

	return flt(result[0][0]) if result else 0


def get_conditions(filters):
	conditions = ""
	if filters.get("employee"):
		conditions += " AND ss.employee = %(employee)s"
	if filters.get("department"):
		conditions += " AND ss.department = %(department)s"
	return conditions


@frappe.whitelist()
def get_heslb_summary(filters: str):
	"""Get HESLB summary for the period"""
	if isinstance(filters, str):
		filters = frappe.parse_json(filters)

	data = get_data(filters)

	total_employees = len(data)
	total_gross = sum(flt(d.get("gross_salary", 0)) for d in data)
	total_deduction = sum(flt(d.get("heslb_deduction", 0)) for d in data)

	return {
		"total_employees": total_employees,
		"total_gross_salary": total_gross,
		"total_heslb_deduction": total_deduction,
		"average_deduction": total_deduction / total_employees if total_employees else 0
	}


@frappe.whitelist()
def export_heslb_excel(filters: str):
	"""Export HESLB data in Excel format for HESLB portal upload"""
	if isinstance(filters, str):
		filters = frappe.parse_json(filters)

	data = get_data(filters)

	# Format for HESLB portal upload
	export_data = []
	for row in data:
		export_data.append({
			"S/N": row.get("sn"),
			"NIDA Number": row.get("nida_no"),
			"Employee Name": row.get("employee_name"),
			"Loan Number": row.get("loan_no"),
			"Gross Salary": row.get("gross_salary"),
			"Deduction Amount": row.get("heslb_deduction"),
			"Pay Period": row.get("pay_period"),
		})

	return export_data
