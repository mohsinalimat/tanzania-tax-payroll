# Copyright (c) 2026, Nelson Mpanju and contributors
# For license information, please see license.txt

"""
VAT eFiling Return Report for TRA
This report generates data in the format required for TRA VAT eFiling submission
"""

import frappe
from frappe import _
from frappe.utils import flt, getdate


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	"""TRA VAT eFiling Return columns"""
	return [
		{
			"fieldname": "section",
			"label": _("Section"),
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"fieldname": "description",
			"label": _("Description"),
			"fieldtype": "Data",
			"width": 350,
		},
		{
			"fieldname": "taxable_amount",
			"label": _("Taxable Amount (TZS)"),
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"fieldname": "vat_amount",
			"label": _("VAT Amount (TZS)"),
			"fieldtype": "Currency",
			"width": 150,
		},
	]


def get_data(filters):
	"""Get VAT data for eFiling return"""
	company = filters.get("company")
	company_abbr = frappe.db.get_value("Company", company, "abbr")
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	# Output VAT account
	output_vat_account = f"Output VAT 18% - {company_abbr}"
	# Input VAT account
	input_vat_account = f"Input VAT 18% - {company_abbr}"

	data = []

	# ============== SECTION A: OUTPUT TAX ==============
	data.append({
		"section": "A",
		"description": "<b>OUTPUT TAX (Sales)</b>",
		"taxable_amount": None,
		"vat_amount": None,
	})

	# A1: Standard Rated Supplies (18%)
	standard_sales = get_standard_rated_sales(company, from_date, to_date, output_vat_account)
	data.append({
		"section": "A1",
		"description": "Standard Rated Supplies (18%)",
		"taxable_amount": standard_sales.get("taxable_amount", 0),
		"vat_amount": standard_sales.get("vat_amount", 0),
	})

	# A2: Zero Rated Supplies
	zero_rated_sales = get_zero_rated_sales(company, from_date, to_date)
	data.append({
		"section": "A2",
		"description": "Zero Rated Supplies (0%)",
		"taxable_amount": zero_rated_sales.get("taxable_amount", 0),
		"vat_amount": 0,
	})

	# A3: Exempt Supplies
	exempt_sales = get_exempt_sales(company, from_date, to_date)
	data.append({
		"section": "A3",
		"description": "Exempt Supplies",
		"taxable_amount": exempt_sales.get("taxable_amount", 0),
		"vat_amount": 0,
	})

	# A4: Total Output Tax
	total_output_vat = standard_sales.get("vat_amount", 0)
	total_output_taxable = (standard_sales.get("taxable_amount", 0) +
						   zero_rated_sales.get("taxable_amount", 0) +
						   exempt_sales.get("taxable_amount", 0))
	data.append({
		"section": "A4",
		"description": "<b>TOTAL OUTPUT TAX</b>",
		"taxable_amount": total_output_taxable,
		"vat_amount": total_output_vat,
	})

	# Empty row separator
	data.append({"section": "", "description": "", "taxable_amount": None, "vat_amount": None})

	# ============== SECTION B: INPUT TAX ==============
	data.append({
		"section": "B",
		"description": "<b>INPUT TAX (Purchases)</b>",
		"taxable_amount": None,
		"vat_amount": None,
	})

	# B1: Local Purchases (18%)
	local_purchases = get_local_purchases(company, from_date, to_date, input_vat_account)
	data.append({
		"section": "B1",
		"description": "Local Purchases (18%)",
		"taxable_amount": local_purchases.get("taxable_amount", 0),
		"vat_amount": local_purchases.get("vat_amount", 0),
	})

	# B2: Imports
	imports = get_imports(company, from_date, to_date, input_vat_account)
	data.append({
		"section": "B2",
		"description": "Imports",
		"taxable_amount": imports.get("taxable_amount", 0),
		"vat_amount": imports.get("vat_amount", 0),
	})

	# B3: Zero Rated Purchases
	zero_rated_purchases = get_zero_rated_purchases(company, from_date, to_date)
	data.append({
		"section": "B3",
		"description": "Zero Rated Purchases",
		"taxable_amount": zero_rated_purchases.get("taxable_amount", 0),
		"vat_amount": 0,
	})

	# B4: Total Input Tax
	total_input_vat = local_purchases.get("vat_amount", 0) + imports.get("vat_amount", 0)
	total_input_taxable = (local_purchases.get("taxable_amount", 0) +
						   imports.get("taxable_amount", 0) +
						   zero_rated_purchases.get("taxable_amount", 0))
	data.append({
		"section": "B4",
		"description": "<b>TOTAL INPUT TAX</b>",
		"taxable_amount": total_input_taxable,
		"vat_amount": total_input_vat,
	})

	# Empty row separator
	data.append({"section": "", "description": "", "taxable_amount": None, "vat_amount": None})

	# ============== SECTION C: NET VAT ==============
	data.append({
		"section": "C",
		"description": "<b>NET VAT CALCULATION</b>",
		"taxable_amount": None,
		"vat_amount": None,
	})

	net_vat = total_output_vat - total_input_vat
	data.append({
		"section": "C1",
		"description": "Output Tax (A4)" if net_vat >= 0 else "Input Tax (B4)",
		"taxable_amount": None,
		"vat_amount": total_output_vat if net_vat >= 0 else total_input_vat,
	})
	data.append({
		"section": "C2",
		"description": "Less: Input Tax (B4)" if net_vat >= 0 else "Less: Output Tax (A4)",
		"taxable_amount": None,
		"vat_amount": total_input_vat if net_vat >= 0 else total_output_vat,
	})
	data.append({
		"section": "C3",
		"description": "<b>VAT PAYABLE TO TRA</b>" if net_vat >= 0 else "<b>VAT REFUND DUE</b>",
		"taxable_amount": None,
		"vat_amount": abs(net_vat),
	})

	return data


def get_standard_rated_sales(company, from_date, to_date, vat_account):
	"""Get standard rated sales (18% VAT)"""
	result = frappe.db.sql("""
		SELECT
			COALESCE(SUM(si.net_total), 0) as taxable_amount,
			COALESCE(SUM(stc.tax_amount), 0) as vat_amount
		FROM `tabSales Invoice` si
		LEFT JOIN `tabSales Taxes and Charges` stc ON stc.parent = si.name
			AND stc.account_head = %s
		WHERE si.company = %s
			AND si.docstatus = 1
			AND si.posting_date BETWEEN %s AND %s
			AND stc.rate = 18
	""", (vat_account, company, from_date, to_date), as_dict=1)

	return result[0] if result else {"taxable_amount": 0, "vat_amount": 0}


def get_zero_rated_sales(company, from_date, to_date):
	"""Get zero rated sales (exports, etc.)"""
	result = frappe.db.sql("""
		SELECT
			COALESCE(SUM(si.net_total), 0) as taxable_amount
		FROM `tabSales Invoice` si
		LEFT JOIN `tabSales Taxes and Charges` stc ON stc.parent = si.name
		WHERE si.company = %s
			AND si.docstatus = 1
			AND si.posting_date BETWEEN %s AND %s
			AND (stc.rate = 0 OR stc.rate IS NULL)
			AND si.net_total > 0
	""", (company, from_date, to_date), as_dict=1)

	return result[0] if result else {"taxable_amount": 0}


def get_exempt_sales(company, from_date, to_date):
	"""Get exempt sales"""
	# Sales without any tax template applied (exempt)
	result = frappe.db.sql("""
		SELECT
			COALESCE(SUM(si.net_total), 0) as taxable_amount
		FROM `tabSales Invoice` si
		WHERE si.company = %s
			AND si.docstatus = 1
			AND si.posting_date BETWEEN %s AND %s
			AND si.taxes_and_charges IS NULL
			AND si.net_total > 0
	""", (company, from_date, to_date), as_dict=1)

	return result[0] if result else {"taxable_amount": 0}


def get_local_purchases(company, from_date, to_date, vat_account):
	"""Get all purchases with VAT (local and imports combined)"""
	result = frappe.db.sql("""
		SELECT
			COALESCE(SUM(pi.net_total), 0) as taxable_amount,
			COALESCE(SUM(ptc.tax_amount), 0) as vat_amount
		FROM `tabPurchase Invoice` pi
		LEFT JOIN `tabPurchase Taxes and Charges` ptc ON ptc.parent = pi.name
			AND ptc.account_head = %s
		WHERE pi.company = %s
			AND pi.docstatus = 1
			AND pi.posting_date BETWEEN %s AND %s
			AND ptc.rate = 18
	""", (vat_account, company, from_date, to_date), as_dict=1)

	return result[0] if result else {"taxable_amount": 0, "vat_amount": 0}


def get_imports(company, from_date, to_date, vat_account):
	"""Get import purchases with VAT - returns 0 as imports are included in local purchases"""
	# Note: is_import field doesn't exist in standard ERPNext
	# All purchases are combined in get_local_purchases
	return {"taxable_amount": 0, "vat_amount": 0}


def get_zero_rated_purchases(company, from_date, to_date):
	"""Get zero rated purchases"""
	result = frappe.db.sql("""
		SELECT
			COALESCE(SUM(pi.net_total), 0) as taxable_amount
		FROM `tabPurchase Invoice` pi
		LEFT JOIN `tabPurchase Taxes and Charges` ptc ON ptc.parent = pi.name
		WHERE pi.company = %s
			AND pi.docstatus = 1
			AND pi.posting_date BETWEEN %s AND %s
			AND (ptc.rate = 0 OR ptc.rate IS NULL)
	""", (company, from_date, to_date), as_dict=1)

	return result[0] if result else {"taxable_amount": 0}


@frappe.whitelist()
def get_vat_summary(filters):
	"""Get VAT summary for the period"""
	if isinstance(filters, str):
		filters = frappe.parse_json(filters)

	company = filters.get("company")
	company_abbr = frappe.db.get_value("Company", company, "abbr")
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	output_vat_account = f"Output VAT 18% - {company_abbr}"
	input_vat_account = f"Input VAT 18% - {company_abbr}"

	standard_sales = get_standard_rated_sales(company, from_date, to_date, output_vat_account)
	local_purchases = get_local_purchases(company, from_date, to_date, input_vat_account)
	imports = get_imports(company, from_date, to_date, input_vat_account)

	total_output = flt(standard_sales.get("vat_amount", 0))
	total_input = flt(local_purchases.get("vat_amount", 0)) + flt(imports.get("vat_amount", 0))
	net_vat = total_output - total_input

	return {
		"total_output_vat": total_output,
		"total_input_vat": total_input,
		"net_vat": net_vat,
		"status": "PAYABLE" if net_vat >= 0 else "REFUND"
	}
