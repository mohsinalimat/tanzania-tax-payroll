"""
Tanzania Payroll Hooks
Handles party assignment for statutory payable accounts in Journal Entries
"""

import frappe
from frappe import _


# Mapping of payable accounts to their respective statutory suppliers
STATUTORY_ACCOUNT_PARTY_MAP = {
	"PAYE Payable": "Tanzania Revenue Authority (TRA)",
	"SDL Payable": "Tanzania Revenue Authority (TRA)",
	"NSSF Payable": "National Social Security Fund (NSSF)",
	"WCF Payable": "Workers Compensation Fund (WCF)",
	"HESLB Payable": "Higher Education Students Loans Board (HESLB)",
}


def before_submit_journal_entry(doc, method):
	"""Add party information to statutory payable accounts in Journal Entry"""
	if not doc.accounts:
		return

	for row in doc.accounts:
		if not row.account:
			continue

		# Check if this is a statutory payable account
		account_name = row.account.split(" - ")[0] if " - " in row.account else row.account

		if account_name in STATUTORY_ACCOUNT_PARTY_MAP:
			# Only set party if not already set
			if not row.party_type and not row.party:
				supplier_name = STATUTORY_ACCOUNT_PARTY_MAP[account_name]

				# Verify supplier exists
				if frappe.db.exists("Supplier", supplier_name):
					row.party_type = "Supplier"
					row.party = supplier_name


def validate_journal_entry(doc, method):
	"""Validate and auto-fill party for statutory payable accounts"""
	if not doc.accounts:
		return

	for row in doc.accounts:
		if not row.account:
			continue

		# Get account type
		account_type = frappe.db.get_value("Account", row.account, "account_type")

		if account_type == "Payable" and not row.party_type:
			# Check if this is a statutory payable account
			account_name = row.account.split(" - ")[0] if " - " in row.account else row.account

			if account_name in STATUTORY_ACCOUNT_PARTY_MAP:
				supplier_name = STATUTORY_ACCOUNT_PARTY_MAP[account_name]

				# Verify supplier exists
				if frappe.db.exists("Supplier", supplier_name):
					row.party_type = "Supplier"
					row.party = supplier_name
