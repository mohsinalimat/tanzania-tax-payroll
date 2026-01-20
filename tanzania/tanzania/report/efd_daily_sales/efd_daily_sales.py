# Copyright (c) 2025, nelson mpanju and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"label": _("Invoice"),
			"fieldname": "invoice",
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 140
		},
		{
			"label": _("Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": _("Time"),
			"fieldname": "posting_time",
			"fieldtype": "Time",
			"width": 80
		},
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 150
		},
		{
			"label": _("Customer TIN"),
			"fieldname": "customer_tin",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Receipt No"),
			"fieldname": "receipt_number",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Net Amount"),
			"fieldname": "net_total",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Tax Amount"),
			"fieldname": "tax_amount",
			"fieldtype": "Currency",
			"width": 110
		},
		{
			"label": _("Grand Total"),
			"fieldname": "grand_total",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Payment Type"),
			"fieldname": "payment_type",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("EFD Status"),
			"fieldname": "efd_status",
			"fieldtype": "Data",
			"width": 90
		},
		{
			"label": _("Verification URL"),
			"fieldname": "verification_url",
			"fieldtype": "Data",
			"width": 200
		},
	]


def get_data(filters):
	conditions = get_conditions(filters)

	data = frappe.db.sql("""
		SELECT
			si.name as invoice,
			si.posting_date,
			si.posting_time,
			si.customer,
			si.customer_tin,
			si.efd_receipt_number as receipt_number,
			si.net_total,
			si.total_taxes_and_charges as tax_amount,
			si.grand_total,
			COALESCE(mop.efd_payment_type, 'CASH') as payment_type,
			si.efd_status,
			si.efd_verification_url as verification_url
		FROM `tabSales Invoice` si
		LEFT JOIN `tabMode of Payment` mop ON si.mode_of_payment = mop.name
		WHERE si.docstatus = 1
			{conditions}
		ORDER BY si.posting_date DESC, si.posting_time DESC
	""".format(conditions=conditions), filters, as_dict=1)

	return data


def get_conditions(filters):
	conditions = ""
	if filters.get("company"):
		conditions += " AND si.company = %(company)s"
	if filters.get("from_date"):
		conditions += " AND si.posting_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += " AND si.posting_date <= %(to_date)s"
	if filters.get("efd_status"):
		conditions += " AND si.efd_status = %(efd_status)s"
	if filters.get("customer"):
		conditions += " AND si.customer = %(customer)s"
	return conditions
