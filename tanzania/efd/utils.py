"""
EFD Utility Functions
Core functions for EFD integration
"""

import frappe
from frappe import _
import json


@frappe.whitelist()
def submit_efd_receipt(invoice_name, preview=False):
	"""Submit Sales Invoice to EFD

	Args:
		invoice_name: Sales Invoice name
		preview: If True, return payload without submitting

	Returns:
		dict: Result with success status and data
	"""
	# Convert string to boolean (from JS frappe.call)
	if isinstance(preview, str):
		preview = preview.lower() in ("true", "1", "yes")

	invoice_doc = frappe.get_doc("Sales Invoice", invoice_name)

	# Validate invoice
	validation = validate_invoice_for_efd(invoice_doc)
	if not validation.get("valid"):
		return {
			"success": False,
			"message": validation.get("message")
		}

	# Get EFD settings
	settings = get_efd_settings(invoice_doc.company)
	if not settings:
		return {
			"success": False,
			"message": _("EFD not configured for company {0}").format(invoice_doc.company)
		}

	if not settings.enabled:
		return {
			"success": False,
			"message": _("EFD is disabled for company {0}").format(invoice_doc.company)
		}

	# Get provider
	from tanzania.efd.providers import get_provider
	provider = get_provider(settings.provider)

	# Build payload
	payload = provider.build_payload(settings, invoice_doc)

	# If preview, return payload
	if preview:
		return {
			"success": True,
			"preview": True,
			"payload": payload,
			"provider": settings.provider
		}

	# Create posting log
	from tanzania.tanzania.doctype.efd_posting_log.efd_posting_log import create_posting_log
	log = create_posting_log(invoice_name, invoice_doc.company, payload)

	# Update invoice status to Pending
	frappe.db.set_value("Sales Invoice", invoice_name, "efd_status", "Pending", update_modified=False)
	frappe.db.set_value("Sales Invoice", invoice_name, "efd_posting_log", log.name, update_modified=False)

	# Submit to provider
	result = provider.post_receipt(settings, invoice_doc, payload)

	# Update posting log
	from tanzania.tanzania.doctype.efd_posting_log.efd_posting_log import update_posting_log

	if result.get("success"):
		data = result.get("data", {})
		update_posting_log(log.name, "Success", result, data)

		# Update invoice with receipt info
		frappe.db.set_value("Sales Invoice", invoice_name, {
			"efd_status": "Success",
			"efd_receipt_number": data.get("receipt_number", ""),
			"efd_verification_url": data.get("verification_url", ""),
			"efd_date": data.get("date"),
			"efd_time": data.get("time"),
		}, update_modified=False)

		frappe.db.commit()

		return {
			"success": True,
			"message": _("EFD receipt submitted successfully"),
			"data": data
		}
	else:
		update_posting_log(log.name, "Failed", result)

		# Update invoice status
		frappe.db.set_value("Sales Invoice", invoice_name, "efd_status", "Failed", update_modified=False)
		frappe.db.commit()

		return {
			"success": False,
			"message": result.get("message", _("Failed to submit EFD receipt")),
			"data": result.get("data")
		}


def validate_invoice_for_efd(invoice_doc):
	"""Validate Sales Invoice for EFD submission

	Args:
		invoice_doc: Sales Invoice document

	Returns:
		dict: {valid: bool, message: str}
	"""
	# Check if already submitted
	if invoice_doc.efd_status == "Success":
		return {
			"valid": False,
			"message": _("Invoice already submitted to EFD")
		}

	# Check if return invoice
	if invoice_doc.is_return:
		return {
			"valid": False,
			"message": _("Return invoices cannot be submitted to EFD")
		}

	# Check if skipped
	if invoice_doc.skip_efd:
		return {
			"valid": False,
			"message": _("Invoice is marked to skip EFD")
		}

	# Check if submitted
	if invoice_doc.docstatus != 1:
		return {
			"valid": False,
			"message": _("Invoice must be submitted before EFD submission")
		}

	# Check if has items
	if not invoice_doc.items:
		return {
			"valid": False,
			"message": _("Invoice has no items")
		}

	# Check total
	if (invoice_doc.grand_total or 0) <= 0:
		return {
			"valid": False,
			"message": _("Invoice total must be greater than zero")
		}

	return {"valid": True}


def get_efd_settings(company):
	"""Get EFD Settings for a company

	Args:
		company: Company name

	Returns:
		EFD Settings document or None
	"""
	if frappe.db.exists("EFD Settings", company):
		return frappe.get_doc("EFD Settings", company)
	return None


def auto_submit_efd(doc, method):
	"""Hook: Auto submit EFD on Sales Invoice submit

	Args:
		doc: Sales Invoice document
		method: Event method name
	"""
	# Check if should auto submit
	if doc.is_return:
		return

	if doc.skip_efd:
		return

	if not doc.auto_submit_efd:
		return

	# Get settings
	settings = get_efd_settings(doc.company)
	if not settings or not settings.enabled:
		return

	if not settings.auto_submit:
		return

	# Check if preview is enabled
	if settings.show_preview:
		# Don't auto-submit if preview is enabled
		# User will manually submit after preview
		return

	# Submit in background
	frappe.enqueue(
		"tanzania.efd.utils.submit_efd_receipt",
		invoice_name=doc.name,
		preview=False,
		queue="short"
	)


def validate_efd_cancel(doc, method):
	"""Hook: Prevent cancellation of EFD-submitted invoices

	Args:
		doc: Sales Invoice document
		method: Event method name
	"""
	if doc.efd_status == "Success" and doc.efd_receipt_number:
		frappe.throw(
			_("Cannot cancel invoice that has been submitted to TRA. "
			  "Receipt Number: {0}").format(doc.efd_receipt_number)
		)


def retry_failed_efd_submissions():
	"""Scheduled task: Retry failed EFD submissions"""
	# Get failed invoices
	failed_invoices = frappe.get_all(
		"Sales Invoice",
		filters={
			"docstatus": 1,
			"efd_status": ["in", ["Pending", "Failed"]],
			"skip_efd": 0,
			"is_return": 0,
		},
		fields=["name", "company"],
		limit=50
	)

	for invoice in failed_invoices:
		# Check retry count
		log = frappe.db.get_value(
			"EFD Posting Log",
			{"sales_invoice": invoice.name},
			["name", "retry_count"],
			as_dict=True
		)

		settings = get_efd_settings(invoice.company)
		max_retries = settings.max_retries if settings else 3

		if log and log.retry_count >= max_retries:
			continue

		try:
			result = submit_efd_receipt(invoice.name)

			# Update retry count
			if log:
				frappe.db.set_value(
					"EFD Posting Log",
					log.name,
					"retry_count",
					(log.retry_count or 0) + 1
				)

		except Exception as e:
			frappe.log_error(
				title=f"EFD Retry Failed: {invoice.name}",
				message=str(e)
			)
