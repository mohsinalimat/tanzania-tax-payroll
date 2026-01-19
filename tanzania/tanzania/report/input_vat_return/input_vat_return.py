# Copyright (c) 2026, Nelson Mpanju and contributors
# For license information, please see license.txt

"""
TRA Input VAT Returns eFiling Report
Lists all purchase invoices with input VAT for TRA submission
"""

import frappe
from frappe import _
from frappe.utils import flt, getdate, formatdate


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	"""TRA Input VAT Return columns based on TRA eFiling format"""
	return [
		{
			"fieldname": "sn",
			"label": _("S/N"),
			"fieldtype": "Int",
			"width": 50,
		},
		{
			"fieldname": "supplier_tin",
			"label": _("Supplier TIN"),
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"fieldname": "supplier_vrn",
			"label": _("Supplier VRN"),
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"fieldname": "supplier_name",
			"label": _("Supplier Name"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "invoice_no",
			"label": _("Invoice No."),
			"fieldtype": "Link",
			"options": "Purchase Invoice",
			"width": 150,
		},
		{
			"fieldname": "invoice_date",
			"label": _("Invoice Date"),
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"fieldname": "description",
			"label": _("Description"),
			"fieldtype": "Data",
			"width": 180,
		},
		{
			"fieldname": "taxable_amount",
			"label": _("Taxable Amount (TZS)"),
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"fieldname": "vat_rate",
			"label": _("VAT Rate (%)"),
			"fieldtype": "Percent",
			"width": 90,
		},
		{
			"fieldname": "vat_amount",
			"label": _("VAT Amount (TZS)"),
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"fieldname": "total_amount",
			"label": _("Total Amount (TZS)"),
			"fieldtype": "Currency",
			"width": 140,
		},
	]


def get_data(filters):
	"""Get Input VAT data from Purchase Invoices"""
	company = filters.get("company")
	company_abbr = frappe.db.get_value("Company", company, "abbr")
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	# Input VAT account
	input_vat_account = f"Input VAT 18% - {company_abbr}"

	conditions = get_conditions(filters)

	# Get purchase invoices with VAT
	invoices = frappe.db.sql("""
		SELECT
			pi.name as invoice_no,
			pi.posting_date as invoice_date,
			pi.supplier,
			pi.supplier_name,
			s.tin as supplier_tin,
			s.vrn as supplier_vrn,
			pi.net_total as taxable_amount,
			pi.grand_total as total_amount,
			pi.bill_no,
			ptc.rate as vat_rate,
			ptc.tax_amount as vat_amount,
			ptc.description
		FROM `tabPurchase Invoice` pi
		INNER JOIN `tabPurchase Taxes and Charges` ptc ON ptc.parent = pi.name
		LEFT JOIN `tabSupplier` s ON pi.supplier = s.name
		WHERE pi.company = %(company)s
			AND pi.docstatus = 1
			AND pi.posting_date BETWEEN %(from_date)s AND %(to_date)s
			AND ptc.account_head = %(vat_account)s
			AND ptc.tax_amount > 0
			{conditions}
		ORDER BY pi.posting_date, pi.name
	""".format(conditions=conditions), {
		"company": company,
		"from_date": from_date,
		"to_date": to_date,
		"vat_account": input_vat_account,
		"supplier": filters.get("supplier"),
	}, as_dict=1)

	data = []
	sn = 0

	for inv in invoices:
		sn += 1
		data.append({
			"sn": sn,
			"supplier_tin": inv.supplier_tin or "",
			"supplier_vrn": inv.supplier_vrn or "",
			"supplier_name": inv.supplier_name,
			"invoice_no": inv.invoice_no,
			"invoice_date": inv.invoice_date,
			"description": inv.description or inv.bill_no or "Purchases",
			"taxable_amount": flt(inv.taxable_amount),
			"vat_rate": flt(inv.vat_rate),
			"vat_amount": flt(inv.vat_amount),
			"total_amount": flt(inv.total_amount),
		})

	return data


def get_conditions(filters):
	conditions = ""
	if filters.get("supplier"):
		conditions += " AND pi.supplier = %(supplier)s"
	return conditions


@frappe.whitelist()
def get_input_vat_summary(filters):
	"""Get summary totals for Input VAT"""
	if isinstance(filters, str):
		filters = frappe.parse_json(filters)

	company = filters.get("company")
	company_abbr = frappe.db.get_value("Company", company, "abbr")
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	input_vat_account = f"Input VAT 18% - {company_abbr}"

	result = frappe.db.sql("""
		SELECT
			COUNT(DISTINCT pi.name) as invoice_count,
			COALESCE(SUM(pi.net_total), 0) as total_taxable,
			COALESCE(SUM(ptc.tax_amount), 0) as total_vat,
			COALESCE(SUM(pi.grand_total), 0) as total_amount
		FROM `tabPurchase Invoice` pi
		INNER JOIN `tabPurchase Taxes and Charges` ptc ON ptc.parent = pi.name
		WHERE pi.company = %s
			AND pi.docstatus = 1
			AND pi.posting_date BETWEEN %s AND %s
			AND ptc.account_head = %s
			AND ptc.tax_amount > 0
	""", (company, from_date, to_date, input_vat_account), as_dict=1)

	return result[0] if result else {
		"invoice_count": 0,
		"total_taxable": 0,
		"total_vat": 0,
		"total_amount": 0
	}
