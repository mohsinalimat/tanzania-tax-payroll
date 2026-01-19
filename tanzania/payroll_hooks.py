"""
Tanzania Payroll Hooks
Handles party assignment for statutory payable accounts in Journal Entries
"""

import frappe
import re
from frappe import _
from frappe.utils import getdate


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
	
	if not employee:
		return  # Can't assign party without employee
	
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
				if hasattr(row, 'reference_type') and row.reference_type == "Salary Slip" and row.reference_name:
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
		if hasattr(row, 'reference_type') and row.reference_type == "Salary Slip" and row.reference_name:
			employee = frappe.db.get_value("Salary Slip", row.reference_name, "employee")
			if employee:
				return employee
	
	# Method 2: Parse date range from user_remark and find salary slips
	# Format: "Accrual Journal Entry for salaries from 2025-02-01 to 2025-02-28"
	user_remark = doc.user_remark or ""
	if "salaries from" in user_remark.lower():
		# Extract dates using regex
		date_pattern = r"from\s+(\d{4}-\d{2}-\d{2})\s+to\s+(\d{4}-\d{2}-\d{2})"
		match = re.search(date_pattern, user_remark)
		
		if match:
			start_date = match.group(1)
			end_date = match.group(2)
			
			# Get company from the JE or first account
			company = doc.company
			if not company and doc.accounts:
				for row in doc.accounts:
					if row.account:
						company = frappe.db.get_value("Account", row.account, "company")
						if company:
							break
			
			if company:
				# Query salary slips in this period
				salary_slips = frappe.get_all(
					"Salary Slip",
					filters={
						"company": company,
						"start_date": [">=", start_date],
						"end_date": ["<=", end_date],
						"docstatus": 1
					},
					pluck="employee",
					limit=1
				)
				
				if salary_slips:
					return salary_slips[0]
	
	return None


