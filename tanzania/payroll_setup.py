"""
Tanzania Payroll Setup
Creates salary components, expense accounts, and default salary structure on app install
"""

import frappe
from frappe import _


def setup_tanzania_payroll(company_name, company_abbr):
	"""Main function to setup Tanzania payroll compliance features"""

	# Create payroll liability accounts
	create_payroll_liability_accounts(company_name, company_abbr)

	# Create payroll expense accounts
	create_payroll_expense_accounts(company_name, company_abbr)

	# Create payroll asset accounts
	create_payroll_asset_accounts(company_name, company_abbr)

	# Create salary components
	create_salary_components(company_name, company_abbr)

	# Create default salary structure
	create_default_salary_structure(company_name, company_abbr)

	frappe.msgprint(_("Tanzania payroll setup completed successfully"))


def create_payroll_expense_accounts(company_name, company_abbr):
	"""Create expense accounts for payroll"""

	# First ensure parent group account exists
	ensure_salaries_wages_group(company_name, company_abbr)

	expense_accounts = [
		{
			"account_name": "Salary and Wages Expenses",
			"parent_account": "Salaries and Wages Accounts",
		},
		{
			"account_name": "Transport Allowance",
			"parent_account": "Salaries and Wages Accounts",
		},
		{
			"account_name": "Leave Encashment",
			"parent_account": "Salaries and Wages Accounts",
		},
		{
			"account_name": "NSSF - Employer Contribution",
			"parent_account": "Salaries and Wages Accounts",
		},
		{
			"account_name": "SDL - Employer Contribution",
			"parent_account": "Salaries and Wages Accounts",
		},
		{
			"account_name": "WCF Expense",
			"parent_account": "Salaries and Wages Accounts",
		},
		{
			"account_name": "PSSF - Employer Contribution",
			"parent_account": "Salaries and Wages Accounts",
		},
		{
			"account_name": "Additional Salary",
			"parent_account": "Salaries and Wages Accounts",
		},
	]

	for account_data in expense_accounts:
		account_name = account_data["account_name"]
		account_name_with_abbr = f"{account_name} - {company_abbr}"

		# Check if account already exists
		if frappe.db.exists("Account", {"account_name": account_name_with_abbr, "company": company_name}):
			continue

		# Get parent account
		parent_account = f"{account_data['parent_account']} - {company_abbr}"

		# Create account
		account_doc = frappe.get_doc({
			"doctype": "Account",
			"company": company_name,
			"account_name": account_name,
			"parent_account": parent_account,
			"is_group": 0,
			"root_type": "Expense",
			"account_type": "Expense Account",
			"report_type": "Profit and Loss",
		})

		account_doc.flags.ignore_links = True
		account_doc.flags.ignore_validate = True
		account_doc.flags.ignore_mandatory = True
		account_doc.insert(ignore_permissions=True, ignore_if_duplicate=True)


def create_payroll_asset_accounts(company_name, company_abbr):
	"""Create asset accounts for payroll (employee advances, loans, deductions)"""

	# First ensure parent group exists
	ensure_loans_advances_group(company_name, company_abbr)

	asset_accounts = [
		{
			"account_name": "Employee Advances",
			"parent_account": "Loans and Advances",
		},
		{
			"account_name": "Employee Loan",
			"parent_account": "Loans and Advances",
		},
		{
			"account_name": "Employee Deductions",
			"parent_account": "Loans and Advances",
		},
	]

	for account_data in asset_accounts:
		account_name = account_data["account_name"]
		account_name_with_abbr = f"{account_name} - {company_abbr}"

		# Check if account already exists
		if frappe.db.exists("Account", {"account_name": account_name_with_abbr, "company": company_name}):
			continue

		# Get parent account
		parent_account = f"{account_data['parent_account']} - {company_abbr}"

		# Create account
		account_doc = frappe.get_doc({
			"doctype": "Account",
			"company": company_name,
			"account_name": account_name,
			"parent_account": parent_account,
			"is_group": 0,
			"root_type": "Asset",
			"account_type": "Receivable",
			"report_type": "Balance Sheet",
		})

		account_doc.flags.ignore_links = True
		account_doc.flags.ignore_validate = True
		account_doc.flags.ignore_mandatory = True
		account_doc.insert(ignore_permissions=True, ignore_if_duplicate=True)


def create_payroll_liability_accounts(company_name, company_abbr):
	"""Create liability accounts for payroll (salaries payable, HESLB, etc.)"""

	# First ensure parent group exists
	ensure_salaries_payable_group(company_name, company_abbr)

	liability_accounts = [
		{
			"account_name": "Payroll Payable",
			"parent_account": "Salaries and Wages Payable",
		},
		{
			"account_name": "HESLB Payable",
			"parent_account": "Salaries and Wages Payable",
		},
	]

	for account_data in liability_accounts:
		account_name = account_data["account_name"]
		account_name_with_abbr = f"{account_name} - {company_abbr}"

		# Check if account already exists
		if frappe.db.exists("Account", {"account_name": account_name_with_abbr, "company": company_name}):
			continue

		# Get parent account
		parent_account = f"{account_data['parent_account']} - {company_abbr}"

		# Create account
		account_doc = frappe.get_doc({
			"doctype": "Account",
			"company": company_name,
			"account_name": account_name,
			"parent_account": parent_account,
			"is_group": 0,
			"root_type": "Liability",
			"account_type": "Payable",
			"report_type": "Balance Sheet",
		})

		account_doc.flags.ignore_links = True
		account_doc.flags.ignore_validate = True
		account_doc.flags.ignore_mandatory = True
		account_doc.insert(ignore_permissions=True, ignore_if_duplicate=True)


def ensure_salaries_wages_group(company_name, company_abbr):
	"""Ensure Salaries and Wages Accounts group exists under Indirect Expenses"""
	group_name = "Salaries and Wages Accounts"
	group_name_with_abbr = f"{group_name} - {company_abbr}"

	if not frappe.db.exists("Account", {"account_name": group_name_with_abbr, "company": company_name}):
		# Must be under Indirect Expenses
		indirect_expenses = f"Indirect Expenses - {company_abbr}"

		# Ensure Indirect Expenses exists first
		if not frappe.db.exists("Account", {"account_name": indirect_expenses, "company": company_name}):
			expense_root = get_root_account(company_name, "Expense")
			frappe.get_doc({
				"doctype": "Account",
				"company": company_name,
				"account_name": "Indirect Expenses",
				"parent_account": expense_root,
				"is_group": 1,
				"root_type": "Expense",
				"account_type": "Expense Account",
				"report_type": "Profit and Loss",
			}).insert(ignore_permissions=True, ignore_if_duplicate=True)

		frappe.get_doc({
			"doctype": "Account",
			"company": company_name,
			"account_name": group_name,
			"parent_account": indirect_expenses,
			"is_group": 1,
			"root_type": "Expense",
			"account_type": "Expense Account",
			"report_type": "Profit and Loss",
		}).insert(ignore_permissions=True, ignore_if_duplicate=True)


def ensure_salaries_payable_group(company_name, company_abbr):
	"""Ensure Salaries and Wages Payable group exists under Current Liabilities"""
	group_name = "Salaries and Wages Payable"
	group_name_with_abbr = f"{group_name} - {company_abbr}"

	if not frappe.db.exists("Account", {"account_name": group_name_with_abbr, "company": company_name}):
		# Must be under Current Liabilities
		current_liabilities = f"Current Liabilities - {company_abbr}"

		# Ensure Current Liabilities exists first
		if not frappe.db.exists("Account", {"account_name": current_liabilities, "company": company_name}):
			liability_root = get_root_account(company_name, "Liability")
			frappe.get_doc({
				"doctype": "Account",
				"company": company_name,
				"account_name": "Current Liabilities",
				"parent_account": liability_root,
				"is_group": 1,
				"root_type": "Liability",
				"account_type": "Payable",
				"report_type": "Balance Sheet",
			}).insert(ignore_permissions=True, ignore_if_duplicate=True)

		frappe.get_doc({
			"doctype": "Account",
			"company": company_name,
			"account_name": group_name,
			"parent_account": current_liabilities,
			"is_group": 1,
			"root_type": "Liability",
			"account_type": "Payable",
			"report_type": "Balance Sheet",
		}).insert(ignore_permissions=True, ignore_if_duplicate=True)


def ensure_loans_advances_group(company_name, company_abbr):
	"""Ensure Loans and Advances group exists under Current Assets"""
	group_name = "Loans and Advances"
	group_name_with_abbr = f"{group_name} - {company_abbr}"

	if not frappe.db.exists("Account", {"account_name": group_name_with_abbr, "company": company_name}):
		# Must be under Current Assets
		current_assets = f"Current Assets - {company_abbr}"

		# Ensure Current Assets exists first
		if not frappe.db.exists("Account", {"account_name": current_assets, "company": company_name}):
			asset_root = get_root_account(company_name, "Asset")
			frappe.get_doc({
				"doctype": "Account",
				"company": company_name,
				"account_name": "Current Assets",
				"parent_account": asset_root,
				"is_group": 1,
				"root_type": "Asset",
				"report_type": "Balance Sheet",
			}).insert(ignore_permissions=True, ignore_if_duplicate=True)

		frappe.get_doc({
			"doctype": "Account",
			"company": company_name,
			"account_name": group_name,
			"parent_account": current_assets,
			"is_group": 1,
			"root_type": "Asset",
			"account_type": "Receivable",
			"report_type": "Balance Sheet",
		}).insert(ignore_permissions=True, ignore_if_duplicate=True)


def get_root_account(company_name, root_type):
	"""Get root account for a given root type"""
	root_accounts = frappe.get_all(
		"Account",
		filters={
			"company": company_name,
			"root_type": root_type,
			"is_group": 1,
			"parent_account": ("is", "not set"),
		},
		limit=1,
	)

	if root_accounts:
		return root_accounts[0].name
	return None


def create_salary_components(company_name, company_abbr):
	"""Create salary components for Tanzania payroll"""

	# Get default cost center
	cost_center = frappe.db.get_value("Company", company_name, "cost_center")

	# Salary components configuration
	salary_components = [
		# ===== EARNINGS =====
		{
			"salary_component": "Basic",
			"salary_component_abbr": "B",
			"description": "Basic Salary",
			"type": "Earning",
			"is_tax_applicable": 1,
			"depends_on_payment_days": 1,
			"formula": "base",
			"amount_based_on_formula": 1,
			"accounts": [
				{
					"company": company_name,
					"account": f"Salary and Wages Expenses - {company_abbr}",
				}
			],
		},
		{
			"salary_component": "Allowance",
			"salary_component_abbr": "IA_1",
			"description": "General Allowance",
			"type": "Earning",
			"is_tax_applicable": 1,
			"depends_on_payment_days": 0,
			"amount_based_on_formula": 0,
			"accounts": [
				{
					"company": company_name,
					"account": f"Salary and Wages Expenses - {company_abbr}",
				}
			],
		},
		{
			"salary_component": "Transport Allowance",
			"salary_component_abbr": "TrAll",
			"description": "Transport Allowance",
			"type": "Earning",
			"is_tax_applicable": 1,
			"depends_on_payment_days": 1,
			"amount_based_on_formula": 0,
			"accounts": [
				{
					"company": company_name,
					"account": f"Transport Allowance - {company_abbr}",
				}
			],
		},
		{
			"salary_component": "Incentives",
			"salary_component_abbr": "Intv",
			"description": "Performance Incentives",
			"type": "Earning",
			"is_tax_applicable": 1,
			"depends_on_payment_days": 0,
			"do_not_include_in_total": 1,
			"amount_based_on_formula": 0,
			"accounts": [
				{
					"company": company_name,
					"account": f"Additional Salary - {company_abbr}",
				}
			],
		},
		{
			"salary_component": "Leave Encashment",
			"salary_component_abbr": "LE",
			"description": "Leave Encashment",
			"type": "Earning",
			"is_tax_applicable": 0,
			"depends_on_payment_days": 1,
			"statistical_component": 1,
			"formula": "base",
			"amount_based_on_formula": 1,
			"accounts": [
				{
					"company": company_name,
					"account": f"Leave Encashment - {company_abbr}",
				}
			],
		},
		# Employer expenses (statistical - not part of employee salary)
		{
			"salary_component": "NSSF Expense",
			"salary_component_abbr": "NSSFe",
			"description": "NSSF Employer Contribution (10%)",
			"type": "Earning",
			"is_tax_applicable": 0,
			"depends_on_payment_days": 0,
			"do_not_include_in_total": 1,
			"condition": "nssf == 1",
			"formula": "(base+IA_1)*0.1",
			"amount_based_on_formula": 1,
			"accounts": [
				{
					"company": company_name,
					"account": f"NSSF - Employer Contribution - {company_abbr}",
				}
			],
		},
		{
			"salary_component": "PSSF Expense",
			"salary_component_abbr": "PSSFe",
			"description": "PSSF Employer Contribution (15%)",
			"type": "Earning",
			"is_tax_applicable": 0,
			"depends_on_payment_days": 0,
			"do_not_include_in_total": 1,
			"condition": "pssf == 1",
			"formula": "(base+IA_1)*0.15",
			"amount_based_on_formula": 1,
			"accounts": [
				{
					"company": company_name,
					"account": f"PSSF - Employer Contribution - {company_abbr}",
				}
			],
		},
		{
			"salary_component": "SDL Expense",
			"salary_component_abbr": "SDLe",
			"description": "Skills Development Levy (3.5%)",
			"type": "Earning",
			"is_tax_applicable": 1,
			"depends_on_payment_days": 0,
			"do_not_include_in_total": 1,
			"formula": "(base+IA_1)*0.035",
			"amount_based_on_formula": 1,
			"accounts": [
				{
					"company": company_name,
					"account": f"SDL - Employer Contribution - {company_abbr}",
				}
			],
		},
		{
			"salary_component": "WCF Expense",
			"salary_component_abbr": "WCFe",
			"description": "Workers Compensation Fund (0.5%)",
			"type": "Earning",
			"is_tax_applicable": 0,
			"depends_on_payment_days": 0,
			"do_not_include_in_total": 1,
			"formula": "(base+IA_1)*0.005",
			"amount_based_on_formula": 1,
			"accounts": [
				{
					"company": company_name,
					"account": f"WCF Expense - {company_abbr}",
				}
			],
		},

		# ===== DEDUCTIONS =====
		{
			"salary_component": "NSSF",
			"salary_component_abbr": "NSSFemp",
			"description": "NSSF Employee Contribution (10%)",
			"type": "Deduction",
			"is_tax_applicable": 0,
			"depends_on_payment_days": 0,
			"condition": "nssf == 1",
			"formula": "(base+IA_1)*0.1",
			"amount_based_on_formula": 1,
			"accounts": [
				{
					"company": company_name,
					"account": f"NSSF Payable - {company_abbr}",
				}
			],
		},
		{
			"salary_component": "NSSF Employer",
			"salary_component_abbr": "NSSFempl",
			"description": "NSSF Employer Contribution (10%)",
			"type": "Deduction",
			"is_tax_applicable": 0,
			"depends_on_payment_days": 0,
			"do_not_include_in_total": 1,
			"condition": "nssf == 1",
			"formula": "(base+IA_1)*0.1",
			"amount_based_on_formula": 1,
			"accounts": [
				{
					"company": company_name,
					"account": f"NSSF Payable - {company_abbr}",
				}
			],
		},
		{
			"salary_component": "PSSF",
			"salary_component_abbr": "PSSFemp",
			"description": "PSSF Employee Contribution (5%)",
			"type": "Deduction",
			"is_tax_applicable": 0,
			"depends_on_payment_days": 0,
			"condition": "pssf == 1",
			"formula": "(base+IA_1)*0.05",
			"amount_based_on_formula": 1,
			"accounts": [
				{
					"company": company_name,
					"account": f"NSSF Payable - {company_abbr}",  # Use NSSF Payable for now (can be changed)
				}
			],
		},
		{
			"salary_component": "PSSF Employer",
			"salary_component_abbr": "PSSFempl",
			"description": "PSSF Employer Contribution (15%)",
			"type": "Deduction",
			"is_tax_applicable": 0,
			"depends_on_payment_days": 0,
			"do_not_include_in_total": 1,
			"condition": "pssf == 1",
			"formula": "(base+IA_1)*0.15",
			"amount_based_on_formula": 1,
			"accounts": [
				{
					"company": company_name,
					"account": f"NSSF Payable - {company_abbr}",  # Use NSSF Payable for now
				}
			],
		},
		{
			"salary_component": "WCF",
			"salary_component_abbr": "WCF",
			"description": "Workers Compensation Fund (0.5%)",
			"type": "Deduction",
			"is_tax_applicable": 0,
			"depends_on_payment_days": 0,
			"do_not_include_in_total": 1,
			"formula": "(base+IA_1)*0.005",
			"amount_based_on_formula": 1,
			"accounts": [
				{
					"company": company_name,
					"account": f"WCF Payable - {company_abbr}",
				}
			],
		},
		{
			"salary_component": "SDL",
			"salary_component_abbr": "SDL",
			"description": "Skills Development Levy (3.5%)",
			"type": "Deduction",
			"is_tax_applicable": 0,
			"depends_on_payment_days": 0,
			"do_not_include_in_total": 1,
			"formula": "(base+IA_1)*0.035",
			"amount_based_on_formula": 1,
			"accounts": [
				{
					"company": company_name,
					"account": f"SDL Payable - {company_abbr}",
				}
			],
		},
		# PAYE Tax Tiers (5 tiers based on Tanzania Income Tax Act)
		{
			"salary_component": "PAYE- (Tax)",
			"salary_component_abbr": "PAYE",
			"description": "PAYE Income Tax",
			"type": "Deduction",
			"is_tax_applicable": 0,
			"depends_on_payment_days": 1,
			"amount_based_on_formula": 0,  # Manual entry or will use multiple tiers
			"accounts": [
				{
					"company": company_name,
					"account": f"PAYE Payable - {company_abbr}",
				}
			],
		},
		# Other deductions
		{
			"salary_component": "HESLB",
			"salary_component_abbr": "HESLB",
			"description": "Higher Education Students Loans Board (15%)",
			"type": "Deduction",
			"is_tax_applicable": 0,
			"depends_on_payment_days": 0,
			"condition": "heslb == 1",
			"formula": "(base+IA_1)*0.15",
			"amount_based_on_formula": 1,
			"accounts": [
				{
					"company": company_name,
					"account": f"HESLB Payable - {company_abbr}",
				}
			],
		},
		{
			"salary_component": "Salary Advance",
			"salary_component_abbr": "SLADV",
			"description": "Salary Advance Recovery",
			"type": "Deduction",
			"is_tax_applicable": 0,
			"depends_on_payment_days": 1,
			"do_not_include_in_total": 1,
			"amount_based_on_formula": 0,
			"accounts": [
				{
					"company": company_name,
					"account": f"Employee Advances - {company_abbr}",
				}
			],
		},
		{
			"salary_component": "Loan",
			"salary_component_abbr": "Ln",
			"description": "Employee Loan Recovery",
			"type": "Deduction",
			"is_tax_applicable": 0,
			"depends_on_payment_days": 1,
			"amount_based_on_formula": 0,
			"accounts": [
				{
					"company": company_name,
					"account": f"Employee Loan - {company_abbr}",
				}
			],
		},
		{
			"salary_component": "Employee Deduction",
			"salary_component_abbr": "ED",
			"description": "Other Employee Deductions",
			"type": "Deduction",
			"is_tax_applicable": 0,
			"depends_on_payment_days": 1,
			"amount_based_on_formula": 0,
			"accounts": [
				{
					"company": company_name,
					"account": f"Employee Deductions - {company_abbr}",
				}
			],
		},
	]

	for component_data in salary_components:
		component_name = component_data["salary_component"]

		# Check if component already exists
		if frappe.db.exists("Salary Component", component_name):
			continue

		# Create salary component
		component_doc = frappe.get_doc({
			"doctype": "Salary Component",
			"salary_component": component_name,
			"salary_component_abbr": component_data.get("salary_component_abbr"),
			"description": component_data.get("description"),
			"type": component_data["type"],
			"is_tax_applicable": component_data.get("is_tax_applicable", 0),
			"depends_on_payment_days": component_data.get("depends_on_payment_days", 0),
			"statistical_component": component_data.get("statistical_component", 0),
			"do_not_include_in_total": component_data.get("do_not_include_in_total", 0),
			"condition": component_data.get("condition", ""),
			"formula": component_data.get("formula", ""),
			"amount_based_on_formula": component_data.get("amount_based_on_formula", 0),
		})

		# Add accounts
		for account in component_data.get("accounts", []):
			component_doc.append("accounts", {
				"company": account["company"],
				"account": account["account"],
			})

		component_doc.flags.ignore_links = True
		component_doc.flags.ignore_validate = True
		component_doc.flags.ignore_mandatory = True
		component_doc.insert(ignore_permissions=True, ignore_if_duplicate=True)


def create_default_salary_structure(company_name, company_abbr):
	"""Create default Tanzania salary structure template"""

	structure_name = "Tanzania Default Salary Structure"

	# Check if structure already exists
	if frappe.db.exists("Salary Structure", structure_name):
		return

	# Get cost center
	cost_center = frappe.db.get_value("Company", company_name, "cost_center")

	# Create salary structure
	structure_doc = frappe.get_doc({
		"doctype": "Salary Structure",
		"name": structure_name,
		"company": company_name,
		"payroll_frequency": "Monthly",
		"currency": "TZS",
		"is_active": "Yes",
	})

	# Add earnings
	earnings = [
		{"salary_component": "Basic", "abbr": "B", "formula": "base", "amount_based_on_formula": 1, "depends_on_payment_days": 1},
		{"salary_component": "Allowance", "abbr": "IA_1", "amount_based_on_formula": 0},
		{"salary_component": "Transport Allowance", "abbr": "TrAll", "amount_based_on_formula": 0, "depends_on_payment_days": 1},
		{"salary_component": "NSSF Expense", "abbr": "NSSFe", "formula": "(base+IA_1)*0.1", "amount_based_on_formula": 1, "do_not_include_in_total": 1, "condition": "nssf == 1"},
		{"salary_component": "PSSF Expense", "abbr": "PSSFe", "formula": "(base+IA_1)*0.15", "amount_based_on_formula": 1, "do_not_include_in_total": 1, "condition": "pssf == 1"},
		{"salary_component": "SDL Expense", "abbr": "SDLe", "formula": "(base+IA_1)*0.035", "amount_based_on_formula": 1, "do_not_include_in_total": 1},
		{"salary_component": "WCF Expense", "abbr": "WCFe", "formula": "(base+IA_1)*0.005", "amount_based_on_formula": 1, "do_not_include_in_total": 1},
	]

	for idx, earning in enumerate(earnings, 1):
		structure_doc.append("earnings", {
			"idx": idx,
			"salary_component": earning["salary_component"],
			"abbr": earning.get("abbr", ""),
			"formula": earning.get("formula", ""),
			"amount_based_on_formula": earning.get("amount_based_on_formula", 0),
			"depends_on_payment_days": earning.get("depends_on_payment_days", 0),
			"do_not_include_in_total": earning.get("do_not_include_in_total", 0),
			"condition": earning.get("condition", ""),
		})

	# Add deductions (NSSF, PAYE tiers, SDL, WCF, etc.)
	deductions = [
		{"salary_component": "NSSF", "abbr": "NSSFemp", "formula": "(base+IA_1)*0.1", "amount_based_on_formula": 1, "condition": "nssf == 1"},
		{"salary_component": "NSSF Employer", "abbr": "NSSFempl", "formula": "(base+IA_1)*0.1", "amount_based_on_formula": 1, "do_not_include_in_total": 1, "condition": "nssf == 1"},
		{"salary_component": "PSSF", "abbr": "PSSFemp", "formula": "(base+IA_1)*0.05", "amount_based_on_formula": 1, "condition": "pssf == 1"},
		{"salary_component": "PSSF Employer", "abbr": "PSSFempl", "formula": "(base+IA_1)*0.15", "amount_based_on_formula": 1, "do_not_include_in_total": 1, "condition": "pssf == 1"},
		{"salary_component": "WCF", "abbr": "WCF", "formula": "(base+IA_1)*0.005", "amount_based_on_formula": 1, "do_not_include_in_total": 1},
		{"salary_component": "SDL", "abbr": "SDL", "formula": "(base+IA_1)*0.035", "amount_based_on_formula": 1, "do_not_include_in_total": 1},
		# PAYE Tiers
		{"salary_component": "PAYE- (Tax)", "abbr": "PAYE", "formula": "(((base+IA_1) - NSSFemp) - 270000) * 0.08", "amount_based_on_formula": 1, "depends_on_payment_days": 1, "condition": "(((base+IA_1) - NSSFemp) >= 270000) and (((base+IA_1) - NSSFemp) < 520000)"},
		{"salary_component": "PAYE- (Tax)", "abbr": "PAYE", "formula": "((((base+IA_1) - NSSFemp) - 520000) * 0.2) + 20000", "amount_based_on_formula": 1, "depends_on_payment_days": 1, "condition": "(((base+IA_1) - NSSFemp) >= 520000) and (((base+IA_1) - NSSFemp) < 760000)"},
		{"salary_component": "PAYE- (Tax)", "abbr": "PAYE", "formula": "((((base+IA_1) -  NSSFemp) - 760000) * 0.25) + 68000", "amount_based_on_formula": 1, "depends_on_payment_days": 1, "condition": "(((base+IA_1) - NSSFemp) >= 760000) and (((base+IA_1) - NSSFemp) < 1000000)"},
		{"salary_component": "PAYE- (Tax)", "abbr": "PAYE", "formula": "((((base+IA_1)- NSSFemp) - 1000000) * 0.3) + 128000", "amount_based_on_formula": 1, "depends_on_payment_days": 1, "condition": "(((base+IA_1) - NSSFemp) >= 1000000)"},
		{"salary_component": "PAYE- (Tax)", "abbr": "PAYE", "formula": "((base+IA_1) - NSSFemp) * 0.3", "amount_based_on_formula": 1, "depends_on_payment_days": 1, "condition": "employment_type == 'Secondary'"},
		# Other deductions
		{"salary_component": "HESLB", "abbr": "HESLB", "formula": "(base+IA_1) * 0.15", "amount_based_on_formula": 1, "condition": "heslb == 1"},
		{"salary_component": "Salary Advance", "abbr": "SLADV", "amount_based_on_formula": 0, "do_not_include_in_total": 1, "depends_on_payment_days": 1},
		{"salary_component": "Loan", "abbr": "Ln", "amount_based_on_formula": 0, "depends_on_payment_days": 1},
		{"salary_component": "Employee Deduction", "abbr": "ED", "amount_based_on_formula": 0, "depends_on_payment_days": 1},
	]

	for idx, deduction in enumerate(deductions, 1):
		structure_doc.append("deductions", {
			"idx": idx,
			"salary_component": deduction["salary_component"],
			"abbr": deduction.get("abbr", ""),
			"formula": deduction.get("formula", ""),
			"amount_based_on_formula": deduction.get("amount_based_on_formula", 0),
			"depends_on_payment_days": deduction.get("depends_on_payment_days", 0),
			"do_not_include_in_total": deduction.get("do_not_include_in_total", 0),
			"condition": deduction.get("condition", ""),
		})

	structure_doc.flags.ignore_links = True
	structure_doc.flags.ignore_validate = True
	structure_doc.flags.ignore_mandatory = True
	structure_doc.insert(ignore_permissions=True, ignore_if_duplicate=True)

	# Submit the salary structure after creation
	structure_doc.submit()
