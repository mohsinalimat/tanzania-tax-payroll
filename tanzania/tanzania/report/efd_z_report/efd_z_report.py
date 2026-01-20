# Copyright (c) 2025, nelson mpanju and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	summary = get_summary(data)
	chart = get_chart(data)

	return columns, data, None, chart, summary


def get_columns():
	return [
		{
			"label": _("Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": _("Total Receipts"),
			"fieldname": "total_receipts",
			"fieldtype": "Int",
			"width": 120
		},
		{
			"label": _("Gross Sales"),
			"fieldname": "gross_sales",
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"label": _("Tax A (18%)"),
			"fieldname": "tax_a",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Tax B (Special)"),
			"fieldname": "tax_b",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Tax C (Zero)"),
			"fieldname": "tax_c",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Tax D (Relief)"),
			"fieldname": "tax_d",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Tax E (Exempt)"),
			"fieldname": "tax_e",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Total Tax"),
			"fieldname": "total_tax",
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"label": _("Net Sales"),
			"fieldname": "net_sales",
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"label": _("Cash"),
			"fieldname": "cash_amount",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Card"),
			"fieldname": "card_amount",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Mobile"),
			"fieldname": "mobile_amount",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Credit"),
			"fieldname": "credit_amount",
			"fieldtype": "Currency",
			"width": 120
		},
	]


def get_data(filters):
	conditions = get_conditions(filters)

	# Get daily summary of EFD receipts
	data = frappe.db.sql("""
		SELECT
			si.posting_date,
			COUNT(si.name) as total_receipts,
			SUM(si.grand_total) as gross_sales,
			SUM(si.total_taxes_and_charges) as total_tax,
			SUM(si.net_total) as net_sales,
			SUM(CASE WHEN mop.efd_payment_type = 'CASH' THEN si.grand_total ELSE 0 END) as cash_amount,
			SUM(CASE WHEN mop.efd_payment_type = 'CCARD' THEN si.grand_total ELSE 0 END) as card_amount,
			SUM(CASE WHEN mop.efd_payment_type = 'EMONEY' THEN si.grand_total ELSE 0 END) as mobile_amount,
			SUM(CASE WHEN mop.efd_payment_type = 'INVOICE' THEN si.grand_total ELSE 0 END) as credit_amount
		FROM `tabSales Invoice` si
		LEFT JOIN `tabMode of Payment` mop ON si.mode_of_payment = mop.name
		WHERE si.docstatus = 1
			AND si.efd_status = 'Success'
			{conditions}
		GROUP BY si.posting_date
		ORDER BY si.posting_date DESC
	""".format(conditions=conditions), filters, as_dict=1)

	# Get tax breakdown by tax code for each day
	for row in data:
		tax_breakdown = get_tax_breakdown(row.posting_date, filters)
		row.update(tax_breakdown)

	return data


def get_tax_breakdown(posting_date, filters):
	"""Get tax amounts by tax code for a specific date"""
	conditions = ""
	if filters.get("company"):
		conditions += " AND si.company = %(company)s"

	result = frappe.db.sql("""
		SELECT
			COALESCE(itt.efd_tax_code, 'A-Standard 18%') as tax_code,
			SUM(sii.net_amount) as amount
		FROM `tabSales Invoice Item` sii
		JOIN `tabSales Invoice` si ON sii.parent = si.name
		LEFT JOIN `tabItem Tax Template` itt ON sii.item_tax_template = itt.name
		WHERE si.docstatus = 1
			AND si.efd_status = 'Success'
			AND si.posting_date = %(posting_date)s
			{conditions}
		GROUP BY COALESCE(itt.efd_tax_code, 'A-Standard 18%')
	""".format(conditions=conditions), {
		"posting_date": posting_date,
		"company": filters.get("company")
	}, as_dict=1)

	tax_breakdown = {
		"tax_a": 0,
		"tax_b": 0,
		"tax_c": 0,
		"tax_d": 0,
		"tax_e": 0,
	}

	for row in result:
		code = (row.tax_code or "")[:1].upper()
		if code == "A":
			tax_breakdown["tax_a"] = row.amount
		elif code == "B":
			tax_breakdown["tax_b"] = row.amount
		elif code == "C":
			tax_breakdown["tax_c"] = row.amount
		elif code == "D":
			tax_breakdown["tax_d"] = row.amount
		elif code == "E":
			tax_breakdown["tax_e"] = row.amount

	return tax_breakdown


def get_conditions(filters):
	conditions = ""
	if filters.get("company"):
		conditions += " AND si.company = %(company)s"
	if filters.get("from_date"):
		conditions += " AND si.posting_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += " AND si.posting_date <= %(to_date)s"
	return conditions


def get_summary(data):
	if not data:
		return []

	total_receipts = sum(d.get("total_receipts", 0) for d in data)
	total_gross = sum(d.get("gross_sales", 0) or 0 for d in data)
	total_tax = sum(d.get("total_tax", 0) or 0 for d in data)
	total_net = sum(d.get("net_sales", 0) or 0 for d in data)

	return [
		{
			"value": total_receipts,
			"label": _("Total Receipts"),
			"datatype": "Int",
		},
		{
			"value": total_gross,
			"label": _("Gross Sales"),
			"datatype": "Currency",
		},
		{
			"value": total_tax,
			"label": _("Total Tax"),
			"datatype": "Currency",
		},
		{
			"value": total_net,
			"label": _("Net Sales"),
			"datatype": "Currency",
		},
	]


def get_chart(data):
	if not data:
		return None

	labels = [d.get("posting_date").strftime("%d %b") for d in data[-30:]]
	values = [d.get("gross_sales", 0) or 0 for d in data[-30:]]

	return {
		"data": {
			"labels": labels,
			"datasets": [
				{
					"name": _("Daily Sales"),
					"values": values
				}
			]
		},
		"type": "bar",
		"colors": ["#5e64ff"]
	}
