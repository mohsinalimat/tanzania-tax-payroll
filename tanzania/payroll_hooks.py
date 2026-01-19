"""
Tanzania Payroll Hooks
Handles party assignment for statutory payable accounts in Journal Entries
"""

import frappe
from frappe import _


# Statutory payable accounts that need Party assignment
STATUTORY_PAYABLE_ACCOUNTS = [
	"PAYE Payable",
	"SDL Payable",
	"NSSF Payable",
	"WCF Payable",
	"HESLB Payable",
	"PSSF Payable",
]


def before_submit_journal_entry(doc, method):
	"""Add party information to statutory payable accounts in Journal Entry"""
	assign_party_to_statutory_accounts(doc)


def validate_journal_entry(doc, method):
	"""Validate and auto-fill party for statutory payable accounts"""
	assign_party_to_statutory_accounts(doc)


def assign_party_to_statutory_accounts(doc):
	"""Assign Employee as Party for statutory payable accounts in payroll JEs"""
	if not doc.accounts:
		return

	# Try to get employee from the JE context (payroll accrual entries)
	employee = get_employee_from_journal_entry(doc)
	
	for row in doc.accounts:
		if not row.account:
			continue

		# Check if this is a statutory payable account
		account_name = row.account.split(" - ")[0] if " - " in row.account else row.account

		if account_name in STATUTORY_PAYABLE_ACCOUNTS:
			# Only set party if not already set
			if not row.party_type and not row.party:
				# Check if this row has a reference to a salary slip
				row_employee = None
				if row.reference_type == "Salary Slip" and row.reference_name:
					row_employee = frappe.db.get_value("Salary Slip", row.reference_name, "employee")
				
				# Use row-specific employee or fallback to JE-level employee
				party_employee = row_employee or employee
				
				if party_employee and frappe.db.exists("Employee", party_employee):
					row.party_type = "Employee"
					row.party = party_employee


def get_employee_from_journal_entry(doc):
	"""Try to extract employee from Journal Entry context"""
	# Method 1: Check if there's a salary slip reference in any row
	for row in doc.accounts:
		if row.reference_type == "Salary Slip" and row.reference_name:
			employee = frappe.db.get_value("Salary Slip", row.reference_name, "employee")
			if employee:
				return employee
	
	# Method 2: If JE is from Payroll Entry, try to get employee
	# (This works when there's only one employee in the payroll)
	if doc.voucher_type == "Journal Entry" and "salaries" in (doc.user_remark or "").lower():
		# Try to find employee from linked documents
		salary_slips = frappe.get_all(
			"Salary Slip",
			filters={
				"journal_entry": doc.name,
				"docstatus": 1
			},
			pluck="employee",
			limit=1
		)
		if salary_slips:
			return salary_slips[0]
	
	return None

