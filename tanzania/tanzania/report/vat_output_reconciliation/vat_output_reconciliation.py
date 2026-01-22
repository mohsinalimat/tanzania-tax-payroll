# Copyright (c) 2024, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	summary = get_summary(data, filters)

	return columns, data, None, None, summary


def get_columns(filters):
	"""Define report columns"""
	columns = [
		{
			"fieldname": "invoice",
			"label": _("Invoice"),
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 140
		},
		{
			"fieldname": "posting_date",
			"label": _("Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 150
		},
		{
			"fieldname": "customer_tin",
			"label": _("Customer TIN"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "customer_vrn",
			"label": _("Customer VRN"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "net_total",
			"label": _("Taxable Amount"),
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"fieldname": "vat_amount",
			"label": _("VAT Amount"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "grand_total",
			"label": _("Total Amount"),
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"fieldname": "tax_rate",
			"label": _("VAT Rate"),
			"fieldtype": "Data",
			"width": 90
		},
	]

	# Add EFD columns if EFD is enabled
	if filters.get("include_efd") or is_efd_enabled(filters.get("company")):
		columns.extend([
			{
				"fieldname": "efd_status",
				"label": _("EFD Status"),
				"fieldtype": "Data",
				"width": 100
			},
			{
				"fieldname": "efd_receipt_number",
				"label": _("EFD Receipt"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "efd_date",
				"label": _("EFD Date"),
				"fieldtype": "Date",
				"width": 100
			},
		])

	return columns


def get_data(filters):
	"""Get Sales Invoice data with VAT details"""
	conditions = get_conditions(filters)

	data = frappe.db.sql("""
		SELECT
			si.name as invoice,
			si.posting_date,
			si.customer,
			si.customer_name,
			si.customer_tin,
			si.customer_vrn,
			si.net_total,
			si.grand_total,
			si.total_taxes_and_charges as vat_amount,
			si.efd_status,
			si.efd_receipt_number,
			si.efd_date,
			si.currency
		FROM `tabSales Invoice` si
		WHERE si.docstatus = 1
		{conditions}
		ORDER BY si.posting_date, si.name
	""".format(conditions=conditions), filters, as_dict=1)

	# Calculate VAT rate for each invoice
	for row in data:
		if row.net_total and row.net_total > 0:
			vat_rate = (row.vat_amount / row.net_total) * 100
			row["tax_rate"] = "{:.0f}%".format(vat_rate) if vat_rate else "0%"
		else:
			row["tax_rate"] = "0%"

	return data


def get_conditions(filters):
	"""Build SQL conditions from filters"""
	conditions = []

	if filters.get("company"):
		conditions.append("si.company = %(company)s")

	if filters.get("from_date"):
		conditions.append("si.posting_date >= %(from_date)s")

	if filters.get("to_date"):
		conditions.append("si.posting_date <= %(to_date)s")

	if filters.get("customer"):
		conditions.append("si.customer = %(customer)s")

	if filters.get("efd_status"):
		conditions.append("si.efd_status = %(efd_status)s")

	# Only include invoices with taxes (VAT)
	if filters.get("vat_only"):
		conditions.append("si.total_taxes_and_charges > 0")

	return " AND " + " AND ".join(conditions) if conditions else ""


def get_summary(data, filters):
	"""Generate report summary"""
	if not data:
		return []

	total_invoices = len(data)
	total_taxable = sum(d.get("net_total", 0) or 0 for d in data)
	total_vat = sum(d.get("vat_amount", 0) or 0 for d in data)
	total_amount = sum(d.get("grand_total", 0) or 0 for d in data)

	summary = [
		{
			"value": total_invoices,
			"indicator": "Blue",
			"label": _("Total Invoices"),
			"datatype": "Int"
		},
		{
			"value": total_taxable,
			"indicator": "Blue",
			"label": _("Total Taxable Amount"),
			"datatype": "Currency"
		},
		{
			"value": total_vat,
			"indicator": "Green",
			"label": _("Total VAT Collected"),
			"datatype": "Currency"
		},
		{
			"value": total_amount,
			"indicator": "Blue",
			"label": _("Total Invoice Amount"),
			"datatype": "Currency"
		},
	]

	# Add EFD summary if applicable
	if filters.get("include_efd") or is_efd_enabled(filters.get("company")):
		efd_success = len([d for d in data if d.get("efd_status") == "Success"])
		efd_pending = len([d for d in data if d.get("efd_status") in ("Pending", "Not Sent", None, "")])
		efd_failed = len([d for d in data if d.get("efd_status") == "Failed"])

		efd_vat_reported = sum(d.get("vat_amount", 0) or 0 for d in data if d.get("efd_status") == "Success")
		efd_vat_unreported = total_vat - efd_vat_reported

		summary.extend([
			{
				"value": efd_success,
				"indicator": "Green",
				"label": _("EFD Submitted"),
				"datatype": "Int"
			},
			{
				"value": efd_pending + efd_failed,
				"indicator": "Red" if (efd_pending + efd_failed) > 0 else "Grey",
				"label": _("EFD Pending/Failed"),
				"datatype": "Int"
			},
			{
				"value": efd_vat_reported,
				"indicator": "Green",
				"label": _("VAT Reported to TRA"),
				"datatype": "Currency"
			},
			{
				"value": efd_vat_unreported,
				"indicator": "Red" if efd_vat_unreported > 0 else "Grey",
				"label": _("VAT Not Reported"),
				"datatype": "Currency"
			},
		])

	return summary


def is_efd_enabled(company=None):
	"""Check if EFD is enabled for the company"""
	try:
		if company:
			# Check if company has EFD settings
			return frappe.db.exists("EFD Settings", {"company": company, "enabled": 1})
		return frappe.db.exists("EFD Settings", {"enabled": 1})
	except Exception:
		return False
