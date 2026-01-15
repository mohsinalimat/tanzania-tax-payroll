"""
Tanzania Tax and Payroll Compliance Setup
Creates tax accounts, templates, and configurations on app install/migrate
"""

import frappe
from frappe import _
from tanzania.custom_fields import create_tanzania_custom_fields
from tanzania.payroll_setup import setup_tanzania_payroll


def after_install():
	"""Setup Tanzania tax and payroll compliance after app installation"""
	setup_tanzania_taxes()
	setup_tanzania_payroll_system()


def after_migrate():
	"""Setup Tanzania tax and payroll compliance after app migration"""
	setup_tanzania_taxes()
	setup_tanzania_payroll_system()


def setup_tanzania_taxes():
	"""Main function to setup all Tanzania tax compliance features"""
	# Create custom fields first (TIN, VRN, etc.)
	create_tanzania_custom_fields()

	companies = frappe.get_all("Company", filters={"country": "Tanzania"}, fields=["name", "abbr"])

	if not companies:
		# If no Tanzania company exists, setup for all companies
		companies = frappe.get_all("Company", fields=["name", "abbr"])

	if not companies:
		frappe.log_error("No companies found for Tanzania tax setup", "Tanzania Tax Setup")
		return

	# Create tax categories (only once, not per company)
	create_tax_categories()

	for company in companies:
		company_name = company.name
		company_abbr = company.abbr

		# Rename default ERPNext accounts first
		rename_default_accounts(company_name, company_abbr)

		# Create tax accounts
		create_tax_accounts(company_name, company_abbr)

		# Create Sales Tax Templates
		create_sales_tax_templates(company_name, company_abbr)

		# Create Purchase Tax Templates
		create_purchase_tax_templates(company_name, company_abbr)

		# Create Item Tax Templates
		create_item_tax_templates(company_name, company_abbr)

	frappe.db.commit()
	frappe.msgprint(_("Tanzania tax setup completed successfully"))


def setup_tanzania_payroll_system():
	"""Main function to setup all Tanzania payroll compliance features"""
	companies = frappe.get_all("Company", filters={"country": "Tanzania"}, fields=["name", "abbr"])

	if not companies:
		# If no Tanzania company exists, setup for all companies
		companies = frappe.get_all("Company", fields=["name", "abbr"])

	if not companies:
		frappe.log_error("No companies found for Tanzania payroll setup", "Tanzania Payroll Setup")
		return

	for company in companies:
		company_name = company.name
		company_abbr = company.abbr

		# Setup payroll (accounts, components, structure)
		setup_tanzania_payroll(company_name, company_abbr)

	frappe.db.commit()
	frappe.msgprint(_("Tanzania payroll setup completed successfully"))


def rename_default_accounts(company_name, company_abbr):
	"""Rename default ERPNext Tanzania accounts to match our naming convention"""

	# ERPNext creates "Tanzania Tax - {abbr}" by default, rename to "Output VAT 18% - {abbr}"
	old_account_name = f"Tanzania Tax - {company_abbr}"
	new_account_name = "Output VAT 18%"

	if frappe.db.exists("Account", old_account_name):
		try:
			account_doc = frappe.get_doc("Account", old_account_name)
			account_doc.account_name = new_account_name
			account_doc.flags.ignore_links = True
			account_doc.flags.ignore_validate = True
			account_doc.save(ignore_permissions=True)
			frappe.db.commit()
			print(f"✅ Renamed account: '{old_account_name}' → 'Output VAT 18% - {company_abbr}'")
		except Exception as e:
			frappe.log_error(f"Error renaming account {old_account_name}: {str(e)}", "Tanzania Account Rename")


def rename_default_templates(company_name, company_abbr, template_type="Sales"):
	"""Delete default ERPNext tax templates - we'll create our own"""

	if template_type == "Sales":
		doctype = "Sales Taxes and Charges Template"
		old_name = f"Tanzania Tax - {company_abbr}"
	else:  # Purchase
		doctype = "Purchase Taxes and Charges Template"
		old_name = f"Tanzania Tax - {company_abbr}"

	# Just delete the old template - our code will create the new one
	if frappe.db.exists(doctype, old_name):
		try:
			frappe.delete_doc(doctype, old_name, force=True, ignore_permissions=True)
			frappe.db.commit()
			print(f"✅ Deleted old template: '{old_name}'")
		except Exception as e:
			frappe.log_error(f"Error deleting template {old_name}: {str(e)}", "Tanzania Template Delete")


def update_existing_template(doctype, template_name, template_config, cost_center):
	"""Update existing template and remove duplicate rows"""

	try:
		template_doc = frappe.get_doc(doctype, template_name)

		# Remove all existing tax rows
		template_doc.taxes = []

		# Add fresh rows from config (no duplicates)
		for tax in template_config["taxes"]:
			template_doc.append("taxes", tax)

		# Set as default if specified
		if template_config.get("is_default"):
			template_doc.is_default = 1

		template_doc.flags.ignore_links = True
		template_doc.flags.ignore_validate = True
		template_doc.flags.ignore_mandatory = True
		template_doc.save(ignore_permissions=True)
		frappe.db.commit()

		print(f"✅ Updated template: '{template_name}' (removed duplicates)")
	except Exception as e:
		frappe.log_error(f"Error updating template {template_name}: {str(e)}", "Tanzania Template Update")


def create_tax_accounts(company_name, company_abbr):
	"""Create tax accounts with proper root types"""

	# Tax accounts configuration
	# Each account has: account_name (without abbr - ERPNext adds it automatically), root_type, account_type, parent_account
	tax_accounts = [
		# Liability accounts (Output VAT - what we charge customers)
		{
			"account_name": "Output VAT 18%",
			"root_type": "Liability",
			"account_type": "Tax",
			"parent_account": "Duties and Taxes",
		},
		{
			"account_name": "VAT Payable",
			"root_type": "Liability",
			"account_type": "Tax",
			"parent_account": "Duties and Taxes",
		},
		{
			"account_name": "Withholding Tax Payable",
			"root_type": "Liability",
			"account_type": "Tax",
			"parent_account": "Duties and Taxes",
		},
		{
			"account_name": "PAYE Payable",
			"root_type": "Liability",
			"account_type": "Payable",
			"parent_account": "Salaries and Wages Payable",
		},
		{
			"account_name": "SDL Payable",
			"root_type": "Liability",
			"account_type": "Payable",
			"parent_account": "Salaries and Wages Payable",
		},
		{
			"account_name": "NSSF Payable",
			"root_type": "Liability",
			"account_type": "Payable",
			"parent_account": "Salaries and Wages Payable",
		},
		{
			"account_name": "WCF Payable",
			"root_type": "Liability",
			"account_type": "Payable",
			"parent_account": "Salaries and Wages Payable",
		},
		# Asset accounts (Input VAT - what we pay to suppliers)
		{
			"account_name": "Input VAT 18%",
			"root_type": "Asset",
			"account_type": "Tax",
			"parent_account": "Tax Assets",
		},
		{
			"account_name": "VAT Receivable",
			"root_type": "Asset",
			"account_type": "Tax",
			"parent_account": "Tax Assets",
		},
		{
			"account_name": "Withholding Tax Receivable",
			"root_type": "Asset",
			"account_type": "Tax",
			"parent_account": "Tax Assets",
		},
		# Expense accounts (Tax expenses)
		{
			"account_name": "Tax Expenses",
			"root_type": "Expense",
			"account_type": "Expense Account",
			"parent_account": "Indirect Expenses",
		},
	]

	# Ensure parent accounts exist first
	ensure_parent_accounts(company_name, company_abbr)

	for account in tax_accounts:
		account_name = account["account_name"]
		account_name_with_abbr = f"{account_name} - {company_abbr}"

		# Check if account already exists (with abbr appended by ERPNext)
		if frappe.db.exists("Account", {"account_name": account_name_with_abbr, "company": company_name}):
			continue

		# Get parent account (with abbr)
		parent_account = get_or_create_parent_account(
			company_name,
			company_abbr,
			account["parent_account"],
			account["root_type"]
		)

		if not parent_account:
			frappe.log_error(
				f"Parent account {account['parent_account']} not found for {account_name}",
				"Tanzania Tax Account Creation"
			)
			continue

		# Create account (ERPNext will automatically append company abbr)
		account_doc = frappe.get_doc({
			"doctype": "Account",
			"company": company_name,
			"account_name": account_name,  # ERPNext will append abbr automatically
			"parent_account": parent_account,
			"is_group": 0,
			"root_type": account["root_type"],
			"account_type": account["account_type"],
			"report_type": "Balance Sheet" if account["root_type"] in ["Asset", "Liability"] else "Profit and Loss",
		})

		account_doc.flags.ignore_links = True
		account_doc.flags.ignore_validate = True
		account_doc.flags.ignore_mandatory = True
		account_doc.insert(ignore_permissions=True, ignore_if_duplicate=True)


def ensure_parent_accounts(company_name, company_abbr):
	"""Ensure all required parent accounts exist"""

	# Duties and Taxes (Liability)
	duties_taxes = "Duties and Taxes"
	duties_taxes_with_abbr = f"{duties_taxes} - {company_abbr}"
	if not frappe.db.exists("Account", {"account_name": duties_taxes_with_abbr, "company": company_name}):
		liability_root = get_root_account(company_name, "Liability")
		if liability_root:
			frappe.get_doc({
				"doctype": "Account",
				"company": company_name,
				"account_name": duties_taxes,
				"parent_account": liability_root,
				"is_group": 1,
				"root_type": "Liability",
				"account_type": "Tax",
				"report_type": "Balance Sheet",
			}).insert(ignore_permissions=True, ignore_if_duplicate=True)

	# Tax Assets (Asset)
	tax_assets = "Tax Assets"
	tax_assets_with_abbr = f"{tax_assets} - {company_abbr}"
	if not frappe.db.exists("Account", {"account_name": tax_assets_with_abbr, "company": company_name}):
		asset_root = get_root_account(company_name, "Asset")
		if asset_root:
			frappe.get_doc({
				"doctype": "Account",
				"company": company_name,
				"account_name": tax_assets,
				"parent_account": asset_root,
				"is_group": 1,
				"root_type": "Asset",
				"account_type": "Tax",
				"report_type": "Balance Sheet",
			}).insert(ignore_permissions=True, ignore_if_duplicate=True)

	# Current Liabilities (Liability) - needed for Salaries and Wages Payable
	current_liabilities = "Current Liabilities"
	current_liabilities_with_abbr = f"{current_liabilities} - {company_abbr}"
	if not frappe.db.exists("Account", {"account_name": current_liabilities_with_abbr, "company": company_name}):
		liability_root = get_root_account(company_name, "Liability")
		if liability_root:
			frappe.get_doc({
				"doctype": "Account",
				"company": company_name,
				"account_name": current_liabilities,
				"parent_account": liability_root,
				"is_group": 1,
				"root_type": "Liability",
				"account_type": "Payable",
				"report_type": "Balance Sheet",
			}).insert(ignore_permissions=True, ignore_if_duplicate=True)

	# Salaries and Wages Payable (under Current Liabilities)
	salaries_payable = "Salaries and Wages Payable"
	salaries_payable_with_abbr = f"{salaries_payable} - {company_abbr}"
	if not frappe.db.exists("Account", {"account_name": salaries_payable_with_abbr, "company": company_name}):
		current_liabilities_parent = f"Current Liabilities - {company_abbr}"
		frappe.get_doc({
			"doctype": "Account",
			"company": company_name,
			"account_name": salaries_payable,
			"parent_account": current_liabilities_parent,
			"is_group": 1,
			"root_type": "Liability",
			"account_type": "Payable",
			"report_type": "Balance Sheet",
		}).insert(ignore_permissions=True, ignore_if_duplicate=True)


def get_root_account(company_name, root_type):
	"""Get the root account for a given root type (Asset, Liability, Expense, Income, Equity)"""
	# Root accounts have no parent_account (NULL or empty)
	root_accounts = frappe.db.sql("""
		SELECT name
		FROM `tabAccount`
		WHERE company = %s
			AND root_type = %s
			AND (parent_account IS NULL OR parent_account = '')
		LIMIT 1
	""", (company_name, root_type), as_dict=1)

	if root_accounts:
		return root_accounts[0].name
	return None


def get_or_create_parent_account(company_name, company_abbr, parent_account_name, root_type):
	"""Get or create a parent account - returns name with abbr for referencing"""
	parent_account_with_abbr = f"{parent_account_name} - {company_abbr}"

	# Check if account exists (with abbr appended by ERPNext)
	if frappe.db.exists("Account", {"account_name": parent_account_with_abbr, "company": company_name}):
		return parent_account_with_abbr

	# Try to find or create parent account
	if "Duties and Taxes" in parent_account_name:
		# Already created in ensure_parent_accounts, but return with abbr
		return parent_account_with_abbr
	elif "Tax Assets" in parent_account_name:
		# Already created in ensure_parent_accounts, but return with abbr
		return parent_account_with_abbr
	elif "Indirect Expenses" in parent_account_name:
		expense_root = get_root_account(company_name, "Expense")
		if expense_root:
			indirect_exp = "Indirect Expenses"
			indirect_exp_with_abbr = f"{indirect_exp} - {company_abbr}"
			if not frappe.db.exists("Account", {"account_name": indirect_exp_with_abbr, "company": company_name}):
				frappe.get_doc({
					"doctype": "Account",
					"company": company_name,
					"account_name": indirect_exp,  # ERPNext will append abbr automatically
					"parent_account": expense_root,
					"is_group": 1,
					"root_type": "Expense",
					"account_type": "Expense Account",
					"report_type": "Profit and Loss",
				}).insert(ignore_permissions=True, ignore_if_duplicate=True)
			return indirect_exp_with_abbr

	return parent_account_with_abbr


def create_tax_categories():
	"""Create tax categories for Tanzania"""
	tax_categories = [
		{"title": "Standard Rated"},
		{"title": "Zero Rated"},
		{"title": "Exempt"},
		{"title": "Out of Scope"},
	]

	for category in tax_categories:
		if not frappe.db.exists("Tax Category", category["title"]):
			frappe.get_doc({
				"doctype": "Tax Category",
				"title": category["title"],
			}).insert(ignore_permissions=True, ignore_if_duplicate=True)


def create_sales_tax_templates(company_name, company_abbr):
	"""Create or update Sales Taxes and Charges Templates"""

	# First, rename default ERPNext templates if they exist
	rename_default_templates(company_name, company_abbr, "Sales")

	# Get cost center
	cost_center = frappe.db.get_value("Company", company_name, "cost_center")
	if not cost_center:
		cost_center = frappe.get_all("Cost Center", filters={"company": company_name}, limit=1)
		cost_center = cost_center[0].name if cost_center else None

	# Sales Tax Templates
	# Note: title doesn't need abbr - ERPNext adds it automatically
	# account_head references need full name with abbr (as saved by ERPNext)
	sales_templates = [
		{
			"title": "Tanzania VAT 18%",
			"is_default": 1,
			"taxes": [
				{
					"account_head": f"Output VAT 18% - {company_abbr}",
					"rate": 18.0,
					"description": "VAT 18%",
					"charge_type": "On Net Total",
					"category": "Total",
					"cost_center": cost_center,
				}
			],
		},
		{
			"title": "Tanzania Zero Rated",
			"taxes": [
				{
					"account_head": f"Output VAT 18% - {company_abbr}",
					"rate": 0.0,
					"description": "VAT 0%",
					"charge_type": "On Net Total",
					"category": "Total",
					"cost_center": cost_center,
				}
			],
		},
	]

	for template in sales_templates:
		template_name = template["title"]
		template_name_with_abbr = f"{template_name} - {company_abbr}"

		# Check if template exists
		if frappe.db.exists("Sales Taxes and Charges Template", {"title": template_name_with_abbr, "company": company_name}):
			# Update existing template - remove duplicates
			update_existing_template("Sales Taxes and Charges Template", template_name_with_abbr, template, cost_center)
			continue

		template_doc = frappe.get_doc({
			"doctype": "Sales Taxes and Charges Template",
			"company": company_name,
			"title": template_name,
			"is_default": template.get("is_default", 0),
		})

		for tax in template["taxes"]:
			template_doc.append("taxes", tax)

		template_doc.flags.ignore_links = True
		template_doc.flags.ignore_validate = True
		template_doc.flags.ignore_mandatory = True
		template_doc.insert(ignore_permissions=True, ignore_if_duplicate=True)


def create_purchase_tax_templates(company_name, company_abbr):
	"""Create or update Purchase Taxes and Charges Templates"""

	# First, rename default ERPNext templates if they exist
	rename_default_templates(company_name, company_abbr, "Purchase")

	# Get cost center
	cost_center = frappe.db.get_value("Company", company_name, "cost_center")
	if not cost_center:
		cost_center = frappe.get_all("Cost Center", filters={"company": company_name}, limit=1)
		cost_center = cost_center[0].name if cost_center else None

	# Purchase Tax Templates
	# Note: title doesn't need abbr - ERPNext adds it automatically
	# account_head references need full name with abbr (as saved by ERPNext)
	purchase_templates = [
		{
			"title": "Tanzania Purchase VAT 18%",
			"is_default": 1,
			"taxes": [
				{
					"account_head": f"Input VAT 18% - {company_abbr}",
					"rate": 18.0,
					"description": "VAT 18%",
					"charge_type": "On Net Total",
					"category": "Total",
					"add_deduct_tax": "Add",
					"cost_center": cost_center,
				}
			],
		},
		{
			"title": "Tanzania Purchase Zero Rated",
			"taxes": [
				{
					"account_head": f"Input VAT 18% - {company_abbr}",
					"rate": 0.0,
					"description": "VAT 0%",
					"charge_type": "On Net Total",
					"category": "Total",
					"add_deduct_tax": "Add",
					"cost_center": cost_center,
				}
			],
		},
	]

	for template in purchase_templates:
		template_name = template["title"]
		template_name_with_abbr = f"{template_name} - {company_abbr}"

		# Check if template exists
		if frappe.db.exists("Purchase Taxes and Charges Template", {"title": template_name_with_abbr, "company": company_name}):
			# Update existing template - remove duplicates
			update_existing_template("Purchase Taxes and Charges Template", template_name_with_abbr, template, cost_center)
			continue

		template_doc = frappe.get_doc({
			"doctype": "Purchase Taxes and Charges Template",
			"company": company_name,
			"title": template_name,
			"is_default": template.get("is_default", 0),
		})

		for tax in template["taxes"]:
			template_doc.append("taxes", tax)

		template_doc.flags.ignore_links = True
		template_doc.flags.ignore_validate = True
		template_doc.flags.ignore_mandatory = True
		template_doc.insert(ignore_permissions=True, ignore_if_duplicate=True)


def create_item_tax_templates(company_name, company_abbr):
	"""Create Item Tax Templates"""

	# Item Tax Templates
	# Note: title doesn't need abbr - ERPNext adds it automatically via autoname
	# tax_type references need full name with abbr (as saved by ERPNext)
	item_tax_templates = [
		{
			"title": "Tanzania VAT 18%",
			"taxes": [
				{
					"tax_type": f"Output VAT 18% - {company_abbr}",
					"tax_rate": 18.0,
				}
			],
		},
		{
			"title": "Tanzania Zero Rated",
			"taxes": [
				{
					"tax_type": f"Output VAT 18% - {company_abbr}",
					"tax_rate": 0.0,
				}
			],
		},
		{
			"title": "Tanzania Exempt",
			"taxes": [
				{
					"tax_type": f"Output VAT 18% - {company_abbr}",
					"tax_rate": 0.0,
				}
			],
		},
	]

	for template in item_tax_templates:
		template_name = template["title"]
		# Item Tax Template uses autoname, so it will have format: {title}-{company_abbr}

		# Check if already exists (fuzzy match by title and company)
		existing = frappe.db.exists("Item Tax Template", {
			"title": template_name,
			"company": company_name
		})

		if existing:
			continue

		template_doc = frappe.get_doc({
			"doctype": "Item Tax Template",
			"company": company_name,
			"title": template_name,
		})

		for tax in template["taxes"]:
			template_doc.append("taxes", tax)

		template_doc.flags.ignore_links = True
		template_doc.flags.ignore_validate = True
		template_doc.insert(ignore_permissions=True, ignore_if_duplicate=True)
