"""
Tanzania Tax and Payroll Compliance Setup
Creates tax accounts, templates, and configurations on app install/migrate
"""

import frappe
from frappe import _


def after_install():
	"""Setup Tanzania tax compliance after app installation"""
	setup_tanzania_taxes()


def after_migrate():
	"""Setup Tanzania tax compliance after app migration"""
	setup_tanzania_taxes()


def setup_tanzania_taxes():
	"""Main function to setup all Tanzania tax compliance features"""
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
		
		# Create tax accounts
		create_tax_accounts(company_name, company_abbr)
		
		# Create Sales Tax Templates
		create_sales_tax_templates(company_name, company_abbr)
		
		# Create Purchase Tax Templates
		create_purchase_tax_templates(company_name, company_abbr)
		
		# Create Item Tax Templates
		create_item_tax_templates(company_name, company_abbr)
	
	frappe.db.commit()
	frappe.msgprint(_("Tanzania tax compliance setup completed successfully"))


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
			"account_type": "Tax",
			"parent_account": "Duties and Taxes",
		},
		{
			"account_name": "SDL Payable",
			"root_type": "Liability",
			"account_type": "Tax",
			"parent_account": "Duties and Taxes",
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
	
	# Create tax accounts
	for account_data in tax_accounts:
		account_name = account_data["account_name"]
		account_name_with_abbr = f"{account_name} - {company_abbr}"
		
		# Check if account already exists (with abbr appended by ERPNext)
		if frappe.db.exists("Account", {"account_name": account_name_with_abbr, "company": company_name}):
			continue
		
		# Get or create parent account (returns name with abbr)
		parent_account = get_or_create_parent_account(
			company_name, 
			company_abbr, 
			account_data["parent_account"],
			account_data["root_type"]
		)
		
		# Create account (ERPNext will automatically append company_abbr)
		account_doc = frappe.get_doc({
			"doctype": "Account",
			"company": company_name,
			"account_name": account_name,
			"parent_account": parent_account,
			"is_group": 0,
			"root_type": account_data["root_type"],
			"account_type": account_data["account_type"],
			"report_type": "Balance Sheet" if account_data["root_type"] in ["Asset", "Liability"] else "Profit and Loss",
		})
		
		account_doc.flags.ignore_links = True
		account_doc.flags.ignore_validate = True
		account_doc.flags.ignore_mandatory = True
		account_doc.insert(ignore_permissions=True, ignore_if_duplicate=True)


def ensure_parent_accounts(company_name, company_abbr):
	"""Ensure parent tax group accounts exist"""
	
	# Duties and Taxes (Liability)
	duties_taxes = "Duties and Taxes"
	duties_taxes_with_abbr = f"{duties_taxes} - {company_abbr}"
	if not frappe.db.exists("Account", {"account_name": duties_taxes_with_abbr, "company": company_name}):
		liability_root = get_root_account(company_name, "Liability")
		if liability_root:
			frappe.get_doc({
				"doctype": "Account",
				"company": company_name,
				"account_name": duties_taxes,  # ERPNext will append abbr automatically
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
				"account_name": tax_assets,  # ERPNext will append abbr automatically
				"parent_account": asset_root,
				"is_group": 1,
				"root_type": "Asset",
				"account_type": "Tax",
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
	"""Create Sales Taxes and Charges Templates"""
	
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
		if frappe.db.exists("Sales Taxes and Charges Template", {"title": template_name_with_abbr, "company": company_name}):
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
	"""Create Purchase Taxes and Charges Templates"""
	
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
		if frappe.db.exists("Purchase Taxes and Charges Template", {"title": template_name_with_abbr, "company": company_name}):
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
		{
			"title": "Tanzania Purchase VAT 18%",
			"taxes": [
				{
					"tax_type": f"Input VAT 18% - {company_abbr}",
					"tax_rate": 18.0,
				}
			],
		},
		{
			"title": "Tanzania Purchase Zero Rated",
			"taxes": [
				{
					"tax_type": f"Input VAT 18% - {company_abbr}",
					"tax_rate": 0.0,
				}
			],
		},
	]
	
	for template in item_tax_templates:
		template_name = template["title"]
		# Item Tax Template autoname adds company abbr, so check with abbr
		template_name_with_abbr = f"{template_name} - {company_abbr}"
		if frappe.db.exists("Item Tax Template", {"title": template_name_with_abbr, "company": company_name}):
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
