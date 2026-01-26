# Copyright (c) 2026, Nelson Mpanju and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate, formatdate


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	"""ITX.219.03.E Statement of Tax Withheld columns based on TRA format"""
	return [
		{
			"fieldname": "sn",
			"label": _("S/N"),
			"fieldtype": "Int",
			"width": 50,
		},
		{
			"fieldname": "tin",
			"label": _("TIN of Withholdee"),
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"fieldname": "withholdee_name",
			"label": _("Name of Withholdee"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "payment_date",
			"label": _("Date of Payment"),
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"fieldname": "nature_of_payment",
			"label": _("Nature of Payment"),
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"fieldname": "gross_amount",
			"label": _("Gross Amount (TZS)"),
			"fieldtype": "Currency",
			"width": 130,
		},
		{
			"fieldname": "wht_rate",
			"label": _("WHT Rate (%)"),
			"fieldtype": "Percent",
			"width": 90,
		},
		{
			"fieldname": "wht_amount",
			"label": _("WHT Amount (TZS)"),
			"fieldtype": "Currency",
			"width": 130,
		},
		{
			"fieldname": "certificate_no",
			"label": _("Certificate No."),
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"fieldname": "invoice_no",
			"label": _("Invoice/Voucher No."),
			"fieldtype": "Link",
			"options": "Purchase Invoice",
			"width": 150,
		},
	]


def get_data(filters):
	"""Get withholding tax data from Purchase Invoices and Payment Entries"""
	conditions = get_conditions(filters)
	company = filters.get("company")
	company_abbr = frappe.db.get_value("Company", company, "abbr")

	# Withholding Tax accounts
	wht_payable_account = f"Withholding Tax Payable - {company_abbr}"

	data = []
	sn = 0

	# Get from Purchase Invoices with WHT
	invoices = frappe.db.sql("""
		SELECT
			pi.name as invoice_no,
			pi.posting_date as payment_date,
			pi.supplier as supplier_id,
			pi.supplier_name as withholdee_name,
			s.tin,
			pi.grand_total,
			pi.net_total,
			pitc.tax_amount as wht_amount,
			pitc.rate as wht_rate,
			pitc.description as nature_of_payment
		FROM `tabPurchase Invoice` pi
		INNER JOIN `tabPurchase Taxes and Charges` pitc ON pitc.parent = pi.name
		LEFT JOIN `tabSupplier` s ON pi.supplier = s.name
		WHERE pi.docstatus = 1
			AND pitc.account_head LIKE %(wht_account)s
			AND pitc.tax_amount != 0
			{conditions}
		ORDER BY pi.posting_date, pi.name
	""".format(conditions=conditions), {
		"company": company,
		"from_date": filters.get("from_date"),
		"to_date": filters.get("to_date"),
		"supplier_filter": filters.get("supplier"),
		"wht_account": f"%Withholding%{company_abbr}%"
	}, as_dict=1)

	for inv in invoices:
		sn += 1
		data.append({
			"sn": sn,
			"tin": inv.tin or "",
			"withholdee_name": inv.withholdee_name,
			"payment_date": inv.payment_date,
			"nature_of_payment": inv.nature_of_payment or "Service Fee",
			"gross_amount": flt(inv.net_total),
			"wht_rate": flt(inv.wht_rate),
			"wht_amount": abs(flt(inv.wht_amount)),
			"certificate_no": "",  # To be filled manually or from custom field
			"invoice_no": inv.invoice_no,
		})

	# Also check GL Entries for WHT transactions
	gl_entries = frappe.db.sql("""
		SELECT
			gl.posting_date as payment_date,
			gl.party,
			gl.party_type,
			gl.voucher_no,
			gl.voucher_type,
			gl.credit as wht_amount,
			gl.remarks as nature_of_payment
		FROM `tabGL Entry` gl
		WHERE gl.account LIKE %s
			AND gl.company = %s
			AND gl.posting_date BETWEEN %s AND %s
			AND gl.credit > 0
			AND gl.is_cancelled = 0
			AND gl.voucher_type NOT IN ('Purchase Invoice')
		ORDER BY gl.posting_date
	""", (f"%Withholding Tax Payable%{company_abbr}%", company,
		  filters.get("from_date"), filters.get("to_date")), as_dict=1)

	for gl in gl_entries:
		# Get party TIN
		tin = ""
		party_name = gl.party or ""
		if gl.party_type == "Supplier" and gl.party:
			supplier_data = frappe.db.get_value("Supplier", gl.party, ["tin", "supplier_name"], as_dict=1)
			if supplier_data:
				tin = supplier_data.tin or ""
				party_name = supplier_data.supplier_name or gl.party

		sn += 1
		data.append({
			"sn": sn,
			"tin": tin,
			"withholdee_name": party_name,
			"payment_date": gl.posting_date,
			"nature_of_payment": gl.nature_of_payment or "Payment",
			"gross_amount": 0,  # Not available from GL
			"wht_rate": 0,
			"wht_amount": flt(gl.wht_amount),
			"certificate_no": "",
			"invoice_no": gl.voucher_no,
		})

	return data


def get_conditions(filters):
	conditions = ""
	if filters.get("company"):
		conditions += " AND pi.company = %(company)s"
	if filters.get("from_date"):
		conditions += " AND pi.posting_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += " AND pi.posting_date <= %(to_date)s"
	if filters.get("supplier"):
		conditions += " AND pi.supplier = %(supplier_filter)s"
	return conditions


@frappe.whitelist()
def get_wht_summary(filters):
	"""Get summary totals for the report"""
	if isinstance(filters, str):
		filters = frappe.parse_json(filters)

	data = get_data(filters)

	total_gross = sum(flt(d.get("gross_amount", 0)) for d in data)
	total_wht = sum(flt(d.get("wht_amount", 0)) for d in data)

	return {
		"total_transactions": len(data),
		"total_gross_amount": total_gross,
		"total_wht_amount": total_wht
	}
