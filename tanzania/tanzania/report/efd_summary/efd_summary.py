# Copyright (c) 2025, nelson mpanju and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	summary = get_summary(filters)
	chart = get_chart(filters)

	return columns, data, None, chart, summary


def get_columns(filters):
	group_by = filters.get("group_by", "Status")

	if group_by == "Status":
		return [
			{"label": _("EFD Status"), "fieldname": "group_field", "fieldtype": "Data", "width": 150},
			{"label": _("Count"), "fieldname": "count", "fieldtype": "Int", "width": 100},
			{"label": _("Net Amount"), "fieldname": "net_total", "fieldtype": "Currency", "width": 140},
			{"label": _("Tax Amount"), "fieldname": "tax_amount", "fieldtype": "Currency", "width": 130},
			{"label": _("Grand Total"), "fieldname": "grand_total", "fieldtype": "Currency", "width": 150},
			{"label": _("Percentage"), "fieldname": "percentage", "fieldtype": "Percent", "width": 100},
		]
	elif group_by == "Payment Type":
		return [
			{"label": _("Payment Type"), "fieldname": "group_field", "fieldtype": "Data", "width": 150},
			{"label": _("Count"), "fieldname": "count", "fieldtype": "Int", "width": 100},
			{"label": _("Net Amount"), "fieldname": "net_total", "fieldtype": "Currency", "width": 140},
			{"label": _("Tax Amount"), "fieldname": "tax_amount", "fieldtype": "Currency", "width": 130},
			{"label": _("Grand Total"), "fieldname": "grand_total", "fieldtype": "Currency", "width": 150},
			{"label": _("Percentage"), "fieldname": "percentage", "fieldtype": "Percent", "width": 100},
		]
	elif group_by == "Tax Code":
		return [
			{"label": _("Tax Code"), "fieldname": "group_field", "fieldtype": "Data", "width": 150},
			{"label": _("Items"), "fieldname": "count", "fieldtype": "Int", "width": 100},
			{"label": _("Net Amount"), "fieldname": "net_total", "fieldtype": "Currency", "width": 140},
			{"label": _("Tax Amount"), "fieldname": "tax_amount", "fieldtype": "Currency", "width": 130},
			{"label": _("Percentage"), "fieldname": "percentage", "fieldtype": "Percent", "width": 100},
		]
	else:  # Monthly
		return [
			{"label": _("Month"), "fieldname": "group_field", "fieldtype": "Data", "width": 120},
			{"label": _("Receipts"), "fieldname": "count", "fieldtype": "Int", "width": 100},
			{"label": _("Net Amount"), "fieldname": "net_total", "fieldtype": "Currency", "width": 140},
			{"label": _("Tax Amount"), "fieldname": "tax_amount", "fieldtype": "Currency", "width": 130},
			{"label": _("Grand Total"), "fieldname": "grand_total", "fieldtype": "Currency", "width": 150},
		]


def get_data(filters):
	group_by = filters.get("group_by", "Status")
	conditions = get_conditions(filters)

	if group_by == "Status":
		data = frappe.db.sql("""
			SELECT
				COALESCE(si.efd_status, 'Not Sent') as group_field,
				COUNT(*) as count,
				SUM(si.net_total) as net_total,
				SUM(si.total_taxes_and_charges) as tax_amount,
				SUM(si.grand_total) as grand_total
			FROM `tabSales Invoice` si
			WHERE si.docstatus = 1
				{conditions}
			GROUP BY COALESCE(si.efd_status, 'Not Sent')
			ORDER BY count DESC
		""".format(conditions=conditions), filters, as_dict=1)

	elif group_by == "Payment Type":
		data = frappe.db.sql("""
			SELECT
				CASE
					WHEN si.is_pos = 1 THEN 'CASH'
					WHEN si.outstanding_amount > 0 THEN 'INVOICE'
					ELSE 'CASH'
				END as group_field,
				COUNT(*) as count,
				SUM(si.net_total) as net_total,
				SUM(si.total_taxes_and_charges) as tax_amount,
				SUM(si.grand_total) as grand_total
			FROM `tabSales Invoice` si
			WHERE si.docstatus = 1
				AND si.efd_status = 'Success'
				{conditions}
			GROUP BY CASE
				WHEN si.is_pos = 1 THEN 'CASH'
				WHEN si.outstanding_amount > 0 THEN 'INVOICE'
				ELSE 'CASH'
			END
			ORDER BY grand_total DESC
		""".format(conditions=conditions), filters, as_dict=1)

	elif group_by == "Tax Code":
		data = frappe.db.sql("""
			SELECT
				COALESCE(itt.efd_tax_code, 'A-Standard 18%') as group_field,
				COUNT(DISTINCT sii.name) as count,
				SUM(sii.net_amount) as net_total,
				SUM(sii.net_amount * COALESCE(
					CASE
						WHEN itt.efd_tax_code LIKE 'A%%' THEN 0.18
						ELSE 0
					END, 0.18
				)) as tax_amount
			FROM `tabSales Invoice Item` sii
			JOIN `tabSales Invoice` si ON sii.parent = si.name
			LEFT JOIN `tabItem Tax Template` itt ON sii.item_tax_template = itt.name
			WHERE si.docstatus = 1
				AND si.efd_status = 'Success'
				{conditions}
			GROUP BY COALESCE(itt.efd_tax_code, 'A-Standard 18%')
			ORDER BY net_total DESC
		""".format(conditions=conditions), filters, as_dict=1)

	else:  # Monthly
		data = frappe.db.sql("""
			SELECT
				DATE_FORMAT(si.posting_date, '%%Y-%%m') as group_field,
				COUNT(*) as count,
				SUM(si.net_total) as net_total,
				SUM(si.total_taxes_and_charges) as tax_amount,
				SUM(si.grand_total) as grand_total
			FROM `tabSales Invoice` si
			WHERE si.docstatus = 1
				AND si.efd_status = 'Success'
				{conditions}
			GROUP BY DATE_FORMAT(si.posting_date, '%%Y-%%m')
			ORDER BY group_field DESC
		""".format(conditions=conditions), filters, as_dict=1)

	# Calculate percentages
	total = sum(d.get("grand_total", 0) or d.get("net_total", 0) or 0 for d in data)
	for row in data:
		amount = row.get("grand_total", 0) or row.get("net_total", 0) or 0
		row["percentage"] = (amount / total * 100) if total else 0

	return data


def get_conditions(filters):
	conditions = ""
	if filters.get("company"):
		conditions += " AND si.company = %(company)s"
	if filters.get("from_date"):
		conditions += " AND si.posting_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += " AND si.posting_date <= %(to_date)s"
	return conditions


def get_summary(filters):
	conditions = get_conditions(filters)

	stats = frappe.db.sql("""
		SELECT
			COUNT(*) as total_invoices,
			SUM(CASE WHEN efd_status = 'Success' THEN 1 ELSE 0 END) as success_count,
			SUM(CASE WHEN efd_status = 'Failed' THEN 1 ELSE 0 END) as failed_count,
			SUM(CASE WHEN efd_status = 'Pending' THEN 1 ELSE 0 END) as pending_count,
			SUM(CASE WHEN COALESCE(efd_status, 'Not Sent') = 'Not Sent' THEN 1 ELSE 0 END) as not_sent_count,
			SUM(CASE WHEN efd_status = 'Success' THEN grand_total ELSE 0 END) as efd_total
		FROM `tabSales Invoice` si
		WHERE si.docstatus = 1
			{conditions}
	""".format(conditions=conditions), filters, as_dict=1)[0]

	success_rate = 0
	if stats.total_invoices:
		success_rate = (stats.success_count or 0) / stats.total_invoices * 100

	return [
		{"value": stats.total_invoices or 0, "label": _("Total Invoices"), "datatype": "Int"},
		{"value": stats.success_count or 0, "label": _("EFD Success"), "datatype": "Int", "indicator": "green"},
		{"value": stats.failed_count or 0, "label": _("EFD Failed"), "datatype": "Int", "indicator": "red"},
		{"value": success_rate, "label": _("Success Rate"), "datatype": "Percent"},
		{"value": stats.efd_total or 0, "label": _("EFD Sales Total"), "datatype": "Currency"},
	]


def get_chart(filters):
	conditions = get_conditions(filters)

	data = frappe.db.sql("""
		SELECT
			COALESCE(si.efd_status, 'Not Sent') as status,
			COUNT(*) as count
		FROM `tabSales Invoice` si
		WHERE si.docstatus = 1
			{conditions}
		GROUP BY COALESCE(si.efd_status, 'Not Sent')
	""".format(conditions=conditions), filters, as_dict=1)

	labels = [d.status for d in data]
	values = [d.count for d in data]

	# Color mapping for statuses
	colors = []
	for label in labels:
		if label == "Success":
			colors.append("#28a745")
		elif label == "Failed":
			colors.append("#dc3545")
		elif label == "Pending":
			colors.append("#ffc107")
		else:
			colors.append("#6c757d")

	return {
		"data": {
			"labels": labels,
			"datasets": [{"name": _("Invoices"), "values": values}]
		},
		"type": "pie",
		"colors": colors
	}
