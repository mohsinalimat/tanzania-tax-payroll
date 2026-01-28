"""
Tanzania Payroll Hooks
Splits consolidated statutory payable entries into individual employee lines
for better audit trail and reference tracking
"""

import frappe
import re
from frappe import _
from frappe.utils import flt


# Statutory payable accounts that need to be split by employee
STATUTORY_PAYABLE_ACCOUNTS = [
	"PAYE Payable",
	"SDL Payable",
	"NSSF Payable",
	"WCF Payable",
	"HESLB Payable",
	"PSSF Payable",
]

# Deduction component to account mapping
DEDUCTION_COMPONENT_MAP = {
	"PAYE": "PAYE Payable",
	"NSSF": "NSSF Payable",
	"NSSF Employee": "NSSF Payable",
	"SDL": "SDL Payable",
	"WCF": "WCF Payable",
	"HESLB": "HESLB Payable",
	"PSSF": "PSSF Payable",
	"PSSF Employee": "PSSF Payable",
}


def validate_journal_entry(doc, method):
	"""Validate journal entry - placeholder for future validations"""
	pass


def before_submit_journal_entry(doc, method):
	"""
	Before submitting a payroll journal entry, split consolidated
	statutory payable lines into individual employee lines
	"""
	# Check if this is a payroll-related journal entry
	if not is_payroll_journal_entry(doc):
		return

	# Get the payroll period from the remark
	period_info = get_payroll_period_from_remark(doc.user_remark or "")
	if not period_info:
		return

	start_date, end_date = period_info

	# Get all salary slips for this period
	salary_slips = get_salary_slips_for_period(doc.company, start_date, end_date)
	if not salary_slips:
		return

	# Split the consolidated statutory lines
	split_statutory_lines(doc, salary_slips)


def is_payroll_journal_entry(doc):
	"""Check if this journal entry is from payroll"""
	user_remark = (doc.user_remark or "").lower()

	# Check for payroll-related remarks
	if "salaries from" in user_remark or "payroll" in user_remark:
		return True

	# Check if accounts contain statutory payables
	for row in doc.accounts:
		if row.account:
			account_name = row.account.split(" - ")[0]
			if account_name in STATUTORY_PAYABLE_ACCOUNTS:
				return True

	return False


def get_payroll_period_from_remark(remark):
	"""Extract start and end date from payroll journal entry remark"""
	# Format: "Accrual Journal Entry for salaries from 2025-01-01 to 2025-01-31"
	date_pattern = r"from\s+(\d{4}-\d{2}-\d{2})\s+to\s+(\d{4}-\d{2}-\d{2})"
	match = re.search(date_pattern, remark)

	if match:
		return match.group(1), match.group(2)

	return None


def get_salary_slips_for_period(company, start_date, end_date):
	"""Get all submitted salary slips for the given period"""
	return frappe.db.sql("""
		SELECT
			ss.name as salary_slip,
			ss.employee,
			ss.employee_name,
			sd.salary_component,
			sd.amount
		FROM `tabSalary Slip` ss
		JOIN `tabSalary Detail` sd ON sd.parent = ss.name
		WHERE ss.company = %s
			AND ss.start_date >= %s
			AND ss.end_date <= %s
			AND ss.docstatus = 1
			AND sd.parentfield = 'deductions'
			AND sd.amount > 0
		ORDER BY ss.employee, sd.salary_component
	""", (company, start_date, end_date), as_dict=True)


def split_statutory_lines(doc, salary_slips):
	"""Split consolidated statutory payable lines into per-employee lines"""

	# Build a mapping of employee deductions
	# {account_name: {employee: amount}}
	employee_deductions = {}

	for slip in salary_slips:
		component = slip.salary_component

		# Find the matching account
		account_base = None
		for comp_key, acc_name in DEDUCTION_COMPONENT_MAP.items():
			if comp_key.lower() in component.lower():
				account_base = acc_name
				break

		if not account_base:
			continue

		if account_base not in employee_deductions:
			employee_deductions[account_base] = {}

		employee = slip.employee
		if employee not in employee_deductions[account_base]:
			employee_deductions[account_base][employee] = {
				"amount": 0,
				"employee_name": slip.employee_name,
				"salary_slip": slip.salary_slip
			}

		employee_deductions[account_base][employee]["amount"] += flt(slip.amount)

	# Now process the journal entry accounts
	# Find and replace consolidated statutory lines with per-employee lines
	new_accounts = []
	processed_accounts = set()

	for row in doc.accounts:
		if not row.account:
			new_accounts.append(row)
			continue

		account_base = row.account.split(" - ")[0]

		# Check if this is a statutory payable that needs splitting
		if account_base in STATUTORY_PAYABLE_ACCOUNTS and account_base in employee_deductions:
			# Skip if already processed (avoid duplicates)
			if account_base in processed_accounts:
				continue

			processed_accounts.add(account_base)

			# Create individual lines for each employee
			for employee, data in employee_deductions[account_base].items():
				if flt(data["amount"]) <= 0:
					continue

				# Determine if this is a debit or credit based on original row
				if flt(row.credit) > 0:
					# Credit entry (payable)
					new_row = {
						"account": row.account,
						"credit_in_account_currency": flt(data["amount"]),
						"credit": flt(data["amount"]),
						"debit_in_account_currency": 0,
						"debit": 0,
						"party_type": "Employee",
						"party": employee,
						"user_remark": f"{account_base} for {data['employee_name']}",
						"cost_center": row.cost_center,
					}
				else:
					# Debit entry
					new_row = {
						"account": row.account,
						"debit_in_account_currency": flt(data["amount"]),
						"debit": flt(data["amount"]),
						"credit_in_account_currency": 0,
						"credit": 0,
						"party_type": "Employee",
						"party": employee,
						"user_remark": f"{account_base} for {data['employee_name']}",
						"cost_center": row.cost_center,
					}

				new_accounts.append(new_row)
		else:
			# Keep non-statutory accounts as-is
			new_accounts.append(row)

	# Replace the accounts
	if new_accounts and processed_accounts:
		doc.accounts = []
		for acc in new_accounts:
			if isinstance(acc, dict):
				doc.append("accounts", acc)
			else:
				# It's an existing row object, convert to dict
				row_dict = {
					"account": acc.account,
					"debit_in_account_currency": acc.debit_in_account_currency,
					"debit": acc.debit,
					"credit_in_account_currency": acc.credit_in_account_currency,
					"credit": acc.credit,
					"cost_center": acc.cost_center,
				}
				# Only include party if set
				if acc.party_type:
					row_dict["party_type"] = acc.party_type
				if acc.party:
					row_dict["party"] = acc.party
				# Only include valid reference types
				if hasattr(acc, 'reference_type') and acc.reference_type in [
					"Sales Invoice", "Purchase Invoice", "Journal Entry",
					"Payroll Entry", "Expense Claim", "Employee Advance"
				]:
					row_dict["reference_type"] = acc.reference_type
					row_dict["reference_name"] = acc.reference_name
				if hasattr(acc, 'user_remark') and acc.user_remark:
					row_dict["user_remark"] = acc.user_remark
				doc.append("accounts", row_dict)
