"""
EFD Posting Log DocType Controller
Audit trail for all EFD submissions to TRA
"""

import frappe
from frappe.model.document import Document


class EFDPostingLog(Document):
	pass


def create_posting_log(sales_invoice, company, request_payload=None):
	"""Create a new EFD Posting Log entry"""
	log = frappe.new_doc("EFD Posting Log")
	log.sales_invoice = sales_invoice
	log.company = company
	log.status = "Pending"
	log.posting_date = frappe.utils.today()
	log.posting_time = frappe.utils.nowtime()
	if request_payload:
		import json
		log.request_payload = json.dumps(request_payload, indent=2)
	log.insert(ignore_permissions=True)
	return log


def update_posting_log(log_name, status, response_data=None, receipt_info=None):
	"""Update EFD Posting Log with response"""
	import json

	log = frappe.get_doc("EFD Posting Log", log_name)
	log.status = status

	if response_data:
		log.response_data = json.dumps(response_data, indent=2)
		log.response_code = str(response_data.get("code", ""))
		log.response_message = response_data.get("message", "")

	if receipt_info:
		log.receipt_number = receipt_info.get("receipt_number", "")
		log.verification_code = receipt_info.get("verification_code", "")
		log.verification_url = receipt_info.get("verification_url", "")
		log.gc_counter = receipt_info.get("gc", 0)
		log.dc_counter = receipt_info.get("dc", 0)

	log.save(ignore_permissions=True)
	return log
