"""
VFDPlus EFD Provider
Integration with VFDPlus API for TRA fiscal receipts
"""

import frappe
from frappe import _
from tanzania.efd.providers.base import BaseEFDProvider


class VFDPlusProvider(BaseEFDProvider):
	"""VFDPlus EFD Provider implementation"""

	name = "VFDPlus"
	base_url_sandbox = "https://sandbox.vfdplus.tz/api/v1"
	base_url_production = "https://api.vfdplus.tz/api/v1"
	timeout = 120

	def get_base_url(self, settings):
		"""Get base URL based on environment"""
		if settings.environment == "Sandbox":
			return self.base_url_sandbox
		return self.base_url_production

	def get_headers(self, settings):
		"""Get request headers with API key"""
		return {
			"Content-Type": "application/json",
			"VFDPLUS-API-KEY": settings.get_password("api_key") or "",
		}

	def get_device_info(self, settings):
		"""Fetch device information from VFDPlus"""
		url = f"{self.get_base_url(settings)}/device/info"
		headers = self.get_headers(settings)

		response = self.make_request(url, method="GET", headers=headers)

		if not response.get("success"):
			return response

		data = response.get("data", {})
		msg_status = data.get("msg_status", "")

		if msg_status == "OK":
			msg_data = data.get("msg_data", {})
			return {
				"success": True,
				"data": {
					"tin": msg_data.get("tin", ""),
					"vrn": msg_data.get("vrn", ""),
					"serial": msg_data.get("serial", ""),
					"company_name": msg_data.get("company_name", ""),
					"address": msg_data.get("address", ""),
					"city": msg_data.get("city", ""),
					"region": msg_data.get("region", ""),
					"tax_office": msg_data.get("taxoffice", ""),
					"registration_id": msg_data.get("account_id", ""),
					"registration_date": msg_data.get("gov_reg_sdate"),
					"expiry_date": msg_data.get("gov_reg_edate"),
					"gc": msg_data.get("gc", 0),
				},
				"message": "Device info fetched successfully"
			}
		else:
			return {
				"success": False,
				"message": data.get("msg", "Failed to fetch device info")
			}

	def post_receipt(self, settings, invoice_doc, payload):
		"""Post fiscal receipt to VFDPlus"""
		url = f"{self.get_base_url(settings)}/receipt/post"
		headers = self.get_headers(settings)

		response = self.make_request(url, method="POST", headers=headers, data=payload)

		if not response.get("success"):
			return response

		data = response.get("data", {})
		msg_status = data.get("msg_status", "")
		msg_code = data.get("msg_code")

		# Success or Warning with duplicate receipt (4015)
		if msg_status == "OK" or (msg_status == "WARNING" and msg_code == 4015):
			msg_data = data.get("msg_data", {})
			receipt_number = msg_data.get("rctvnum", "")
			date_str = msg_data.get("idate", "")
			time_str = msg_data.get("itime", "")

			return {
				"success": True,
				"data": {
					"receipt_number": receipt_number,
					"verification_code": receipt_number,
					"verification_url": self.generate_verification_url(receipt_number, time_str),
					"date": date_str,
					"time": time_str,
					"gc": msg_data.get("gc", 0),
					"dc": msg_data.get("dc", 0),
				},
				"message": "Receipt posted successfully"
			}
		else:
			return {
				"success": False,
				"code": msg_code,
				"message": data.get("msg", "Failed to post receipt"),
				"data": data
			}

	def build_payload(self, settings, invoice_doc):
		"""Build receipt payload for VFDPlus"""
		# Get customer info
		customer_info = self.get_customer_info(invoice_doc.customer)

		# Get serial code
		serial_code = settings.serial_number or ""

		# Format date and time
		date_str, time_str = self.format_datetime(invoice_doc.posting_date)

		# Build cart items
		cart_items = []
		for item in invoice_doc.items:
			tax_info = self.get_item_tax_code(item.item_code, item.item_tax_template)

			# Calculate amount (VFDPlus expects tax-inclusive)
			amount = self.calculate_item_amount(item, tax_info["rate"], is_inclusive=True)
			unit_price = amount / item.qty if item.qty else amount

			cart_items.append({
				"vat_rate_code": tax_info["code"],
				"vat_rate_id": tax_info["id"],
				"item_name": item.item_code,
				"item_barcode": "-1",
				"item_qty": item.qty,
				"usp": round(unit_price, 2),
				"sp": round(amount, 2),
				"unit_discount_perc": 0.0,
				"unit_discount_amt": 0.0,
				"total_item_discount": 0.0,
			})

		# Get payment type
		payment_type = self.get_payment_type(invoice_doc.get("mode_of_payment"))

		# Calculate totals
		total_amount = invoice_doc.grand_total or invoice_doc.rounded_total or 0

		payload = {
			"credential_code": serial_code,
			"branch_id": "",
			"depart_id": "",
			"trans_no": invoice_doc.name,
			"idate": date_str,
			"itime": time_str,
			"customer_info": {
				"cust_name": customer_info["name"],
				"cust_id_type": customer_info["id_type"],
				"cust_id": customer_info["id_value"] or "NIL",
				"cust_phone": "",
				"cust_vrn": customer_info["vrn"],
				"cust_addr": "",
				"id_for": "",
			},
			"payment_methods": [{
				"pmt_type": payment_type,
				"pmt_amount": round(total_amount, 2),
			}],
			"cart_totals": {
				"item_counts": len(cart_items),
				"total_amount": round(total_amount, 2),
				"total_amount_exclude_discount": round(total_amount, 2),
				"discount": 0.0,
			},
			"cart_items": cart_items,
			"user_info": {
				"user_id": "1",
				"username": invoice_doc.modified_by or "Administrator",
				"till_id": "1",
			}
		}

		return payload
