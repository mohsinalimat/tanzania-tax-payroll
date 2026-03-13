"""
Cleanup script to remove duplicate tax templates and rows
Run with: bench --site your-site.com execute tanzania.cleanup_tax_setup.cleanup_all
"""

import frappe

def cleanup_all():
	"""Clean up all tax templates and remove duplicates"""
	companies = frappe.get_all("Company", fields=["name", "abbr"])

	for company in companies:
		company_name = company.name
		company_abbr = company.abbr

		print(f"\n=== Cleaning up tax setup for {company_name} ({company_abbr}) ===")

		# Delete old "Tanzania Tax" templates
		delete_old_templates(company_abbr)

		# Remove duplicate rows from templates
		remove_duplicate_template_rows(company_abbr)

		# Remove duplicate rows from item tax templates
		remove_duplicate_item_tax_rows(company_abbr)

		# Delete old "Tanzania Tax" or "VAT" accounts if they exist
		cleanup_old_accounts(company_abbr)

	frappe.db.commit()  # nosemgrep: frappe-manual-commit - commit needed after bulk cleanup operations
	print("\n✅ Cleanup completed successfully!")


def delete_old_templates(company_abbr):
	"""Delete old 'Tanzania Tax' templates"""

	# Sales Tax Template
	old_sales_template = f"Tanzania Tax - {company_abbr}"
	if frappe.db.exists("Sales Taxes and Charges Template", old_sales_template):
		try:
			frappe.delete_doc("Sales Taxes and Charges Template", old_sales_template, force=True, ignore_permissions=True)
			print(f"✅ Deleted old sales template: {old_sales_template}")
		except Exception as e:
			print(f"⚠️  Could not delete {old_sales_template}: {str(e)}")

	# Purchase Tax Template
	old_purchase_template = f"Tanzania Tax - {company_abbr}"
	if frappe.db.exists("Purchase Taxes and Charges Template", old_purchase_template):
		try:
			frappe.delete_doc("Purchase Taxes and Charges Template", old_purchase_template, force=True, ignore_permissions=True)
			print(f"✅ Deleted old purchase template: {old_purchase_template}")
		except Exception as e:
			print(f"⚠️  Could not delete {old_purchase_template}: {str(e)}")

	# Item Tax Template - Delete old "Tanzania Tax" template
	old_item_tax_template = f"Tanzania Tax - {company_abbr}"
	if frappe.db.exists("Item Tax Template", old_item_tax_template):
		try:
			frappe.delete_doc("Item Tax Template", old_item_tax_template, force=True, ignore_permissions=True)
			print(f"✅ Deleted old item tax template: {old_item_tax_template}")
		except Exception as e:
			print(f"⚠️  Could not delete {old_item_tax_template}: {str(e)}")


def remove_duplicate_template_rows(company_abbr):
	"""Remove duplicate rows from tax templates"""

	# Sales Templates
	sales_templates = [
		f"Tanzania VAT 18% - {company_abbr}",
		f"Tanzania Zero Rated - {company_abbr}",
	]

	for template_name in sales_templates:
		if frappe.db.exists("Sales Taxes and Charges Template", template_name):
			try:
				template_doc = frappe.get_doc("Sales Taxes and Charges Template", template_name)

				# Get unique rows (keep only first occurrence of each account)
				seen_accounts = set()
				unique_rows = []

				for row in template_doc.taxes:
					if row.account_head not in seen_accounts:
						seen_accounts.add(row.account_head)
						unique_rows.append(row)

				# If we have duplicates, remove and re-add
				if len(unique_rows) < len(template_doc.taxes):
					template_doc.taxes = []
					for row in unique_rows:
						template_doc.append("taxes", {
							"account_head": row.account_head,
							"rate": row.rate,
							"description": row.description,
							"charge_type": row.charge_type,
							"cost_center": row.cost_center,
						})

					template_doc.flags.ignore_links = True
					template_doc.flags.ignore_validate = True
					template_doc.save(ignore_permissions=True)
					print(f"✅ Removed duplicates from: {template_name}")
			except Exception as e:
				print(f"⚠️  Error cleaning {template_name}: {str(e)}")

	# Purchase Templates
	purchase_templates = [
		f"Tanzania Purchase VAT 18% - {company_abbr}",
		f"Tanzania Purchase Zero Rated - {company_abbr}",
	]

	for template_name in purchase_templates:
		if frappe.db.exists("Purchase Taxes and Charges Template", template_name):
			try:
				template_doc = frappe.get_doc("Purchase Taxes and Charges Template", template_name)

				# Get unique rows
				seen_accounts = set()
				unique_rows = []

				for row in template_doc.taxes:
					if row.account_head not in seen_accounts:
						seen_accounts.add(row.account_head)
						unique_rows.append(row)

				# If we have duplicates, remove and re-add
				if len(unique_rows) < len(template_doc.taxes):
					template_doc.taxes = []
					for row in unique_rows:
						template_doc.append("taxes", {
							"account_head": row.account_head,
							"rate": row.rate,
							"description": row.description,
							"charge_type": row.charge_type,
							"category": row.category,
							"add_deduct_tax": row.add_deduct_tax,
							"cost_center": row.cost_center,
						})

					template_doc.flags.ignore_links = True
					template_doc.flags.ignore_validate = True
					template_doc.save(ignore_permissions=True)
					print(f"✅ Removed duplicates from: {template_name}")
			except Exception as e:
				print(f"⚠️  Error cleaning {template_name}: {str(e)}")


def remove_duplicate_item_tax_rows(company_abbr):
	"""Remove duplicate rows from Item Tax Templates"""

	item_tax_templates = [
		f"Tanzania VAT 18% - {company_abbr}",
		f"Tanzania Zero Rated - {company_abbr}",
		f"Tanzania Exempt - {company_abbr}",
		f"Tanzania Purchase VAT 18% - {company_abbr}",
		f"Tanzania Purchase Zero Rated - {company_abbr}",
	]

	for template_name in item_tax_templates:
		if frappe.db.exists("Item Tax Template", template_name):
			try:
				template_doc = frappe.get_doc("Item Tax Template", template_name)

				# Get unique rows (keep only first occurrence of each tax_type)
				seen_tax_types = set()
				unique_rows = []

				for row in template_doc.taxes:
					if row.tax_type not in seen_tax_types:
						seen_tax_types.add(row.tax_type)
						unique_rows.append(row)

				# If we have duplicates, remove and re-add
				if len(unique_rows) < len(template_doc.taxes):
					template_doc.taxes = []
					for row in unique_rows:
						template_doc.append("taxes", {
							"tax_type": row.tax_type,
							"tax_rate": row.tax_rate,
						})

					template_doc.flags.ignore_links = True
					template_doc.flags.ignore_validate = True
					template_doc.save(ignore_permissions=True)
					print(f"✅ Removed duplicates from item tax: {template_name}")
			except Exception as e:
				print(f"⚠️  Error cleaning item tax {template_name}: {str(e)}")


def cleanup_old_accounts(company_abbr):
	"""Delete old accounts that are no longer needed"""

	# Old account that might exist
	old_vat_account = f"VAT - {company_abbr}"

	if frappe.db.exists("Account", old_vat_account):
		# Check if it's being used anywhere
		usage_count = frappe.db.count("GL Entry", {"account": old_vat_account})

		if usage_count == 0:
			try:
				frappe.delete_doc("Account", old_vat_account, force=True, ignore_permissions=True)
				print(f"✅ Deleted unused account: {old_vat_account}")
			except Exception as e:
				print(f"⚠️  Could not delete {old_vat_account}: {str(e)}")
		else:
			print(f"ℹ️  Account {old_vat_account} has {usage_count} GL entries, keeping it")
