# Copyright (c) 2026, Nelson Mpanju and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt

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
			"fieldname": "department",
			"label": _("Department"),
			"fieldtype": "Link",
			"options": "Department",
			"width": 180
		},
		{
			"fieldname": "gross_pay",
			"label": _("Gross Pay"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "nssf_employer",
			"label": _("NSSF (Employer)"),
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "pssf_employer",
			"label": _("PSSF (Employer)"),
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "sdl_employer",
			"label": _("SDL (3.5%)"),
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"fieldname": "wcf_employer",
			"label": _("WCF (0.5%)"),
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"fieldname": "total_cost",
			"label": _("Total Cost to Company"),
			"fieldtype": "Currency",
			"width": 180
		}
	]

def get_data(filters):
	conditions = get_conditions(filters)
	
	# Fetch Salary Slips
	data_map = {}
	
	salary_slips = frappe.db.sql("""
		SELECT
			name, department, gross_pay
		FROM `tabSalary Slip`
		WHERE docstatus = 1
	""" + conditions, filters, as_dict=1)

	if not salary_slips:
		return []

	salary_slip_names = [d.name for d in salary_slips]
	
	# Fetch Employer Contributions (Statistical Earnings)
	# Based on payroll_setup.py: 
	# NSSF Expense, PSSF Expense, SDL Expense, WCF Expense
	details = frappe.db.sql("""
		SELECT 
			parent, salary_component, amount
		FROM `tabSalary Detail`
		WHERE 
			parent IN %(names)s 
			AND parentfield = 'earnings'
			AND salary_component IN ('NSSF Expense', 'PSSF Expense', 'SDL Expense', 'WCF Expense')
	""", {"names": salary_slip_names}, as_dict=1)
	
	# Process Salary Slips
	for slip in salary_slips:
		dept = slip.department or _("Unassigned")
		if dept not in data_map:
			data_map[dept] = {
				"department": dept,
				"gross_pay": 0.0,
				"nssf_employer": 0.0,
				"pssf_employer": 0.0,
				"sdl_employer": 0.0,
				"wcf_employer": 0.0,
				"total_cost": 0.0
			}
		
		val = data_map[dept]
		val["gross_pay"] += flt(slip.gross_pay)

	# Process Details for Employer Contributions
	for d in details:
		# Find which department this slip belongs to
		# We need a quick lookup map for slip -> department
		slip_dept_map = {s.name: (s.department or _("Unassigned")) for s in salary_slips}
		
		dept = slip_dept_map.get(d.parent)
		if not dept: continue

		amount = flt(d.amount)
		val = data_map[dept]
		
		if d.salary_component == 'NSSF Expense':
			val["nssf_employer"] += amount
		elif d.salary_component == 'PSSF Expense':
			val["pssf_employer"] += amount
		elif d.salary_component == 'SDL Expense':
			val["sdl_employer"] += amount
		elif d.salary_component == 'WCF Expense':
			val["wcf_employer"] += amount

	# Calculate Total Cost
	result = []
	for dept, val in data_map.items():
		val["total_cost"] = (
			val["gross_pay"] + 
			val["nssf_employer"] + 
			val["pssf_employer"] + 
			val["sdl_employer"] + 
			val["wcf_employer"]
		)
		result.append(val)
	
	return sorted(result, key=lambda x: x['department'])

def get_conditions(filters):
	conditions = []
	if filters.get("company"):
		conditions.append("company = %(company)s")
	if filters.get("from_date"):
		conditions.append("start_date >= %(from_date)s")
	if filters.get("to_date"):
		conditions.append("end_date <= %(to_date)s")
	if filters.get("department"):
		conditions.append("department = %(department)s")
	if filters.get("branch"):
		conditions.append("branch = %(branch)s")
		
	return "AND " + " AND ".join(conditions) if conditions else ""

def get_chart_data(data):
	if not data:
		return None
		
	labels = [d.get("department") for d in data]
	gross_pay = [d.get("gross_pay") for d in data]
	total_cost = [d.get("total_cost") for d in data]
	
	return {
		"data": {
			"labels": labels,
			"datasets": [
				{"name": _("Gross Pay"), "values": gross_pay},
				{"name": _("Total Cost"), "values": total_cost}
			]
		},
		"type": "bar",
		"colors": ["#4da6ff", "#0066cc"]
	}
