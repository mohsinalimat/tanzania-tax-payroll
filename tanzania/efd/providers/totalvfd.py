"""
TotalVFD EFD Provider
Integration with TotalVFD API for TRA fiscal receipts
"""

import frappe
from frappe import _
from tanzania.efd.providers.base import BaseEFDProvider


class TotalVFDProvider(BaseEFDProvider):
	"""TotalVFD EFD Provider implementation"""

	name = "TotalVFD"
	base_url = "https://api.totalvfd.co.tz/api/v1"
	timeout = 120

	def get_headers(self, settings):
		"""Get request headers with bearer token"""
		return {
			"Content-Type": "application/json",
			"Authorization": f"Bearer {settings.get_password('api_key') or ''}",
		}

	def get_device_info(self, settings):
		"""Fetch device information from TotalVFD"""
		url = f"{self.base_url}/device/{settings.serial_number}"
		headers = self.get_headers(settings)

		response = self.make_request(url, method="GET", headers=headers)

		if not response.get("success"):
			return response

		data = response.get("data", {})

		if data.get("status") == 200 or data.get("serial"):
			return {
				"success": True,
				"data": {
					"tin": data.get("tin", ""),
					"vrn": data.get("vrn", ""),
					"serial": data.get("serial", ""),
					"company_name": data.get("companyName", ""),
					"address": data.get("address", ""),
					"city": data.get("city", ""),
					"region": data.get("region", ""),
					"tax_office": data.get("taxOffice", ""),
					"registration_id": data.get("registrationId", ""),
					"registration_date": data.get("registrationDate"),
					"expiry_date": data.get("expiryDate"),
					"gc": data.get("gc", 0),
				},
				"message": "Device info fetched successfully"
			}
		else:
			return {
				"success": False,
				"message": data.get("message", "Failed to fetch device info")
			}

	def post_receipt(self, settings, invoice_doc, payload):
		"""Post fiscal receipt to TotalVFD"""
		url = f"{self.base_url}/receipt"
		headers = self.get_headers(settings)

		response = self.make_request(url, method="POST", headers=headers, data=payload)

		if not response.get("success"):
			return response

		data = response.get("data", {})
		status = data.get("status") or response.get("status_code")

		# Success (200, 201) or Conflict (409 - duplicate)
		if status in [200, 201, 409]:
			receipt_number = data.get("rctvnum", "")
			date_str = data.get("localDate", "")
			time_str = data.get("localTime", "")
			verification_url = data.get("verificationLink", "")

			if not verification_url and receipt_number:
				verification_url = self.generate_verification_url(receipt_number, time_str)

			return {
				"success": True,
				"data": {
					"receipt_number": receipt_number,
					"verification_code": receipt_number,
					"verification_url": verification_url,
					"date": date_str,
					"time": time_str,
					"gc": data.get("gc", 0),
					"dc": data.get("dc", 0),
				},
				"message": "Receipt posted successfully"
			}
		else:
			return {
				"success": False,
				"code": status,
				"message": data.get("message", "Failed to post receipt"),
				"data": data
			}

	def build_payload(self, settings, invoice_doc):
		"""Build receipt payload for TotalVFD"""
		# Get customer info
		customer_info = self.get_customer_info(invoice_doc.customer)

		# Build items
		items = []
		for item in invoice_doc.items:
			tax_info = self.get_item_tax_code(item.item_code, item.item_tax_template)

			# Calculate amount
			amount = self.calculate_item_amount(item, tax_info["rate"], is_inclusive=True)
			unit_price = amount / item.qty if item.qty else amount

			items.append({
				"id": item.item_code,
				"name": item.item_name or item.item_code,
				"price": round(unit_price, 2),
				"qty": item.qty,
				"vatGroup": tax_info["code"],
				"discount": 0.0,
			})

		# Get payment type
		payment_type = self.get_payment_type(invoice_doc.get("mode_of_payment"))

		# Calculate totals
		total_amount = invoice_doc.grand_total or invoice_doc.rounded_total or 0

		payload = {
			"serial": settings.serial_number or "",
			"referenceNumber": invoice_doc.name,
			"customer": {
				"name": customer_info["name"],
				"idType": customer_info["id_type"],
				"idValue": customer_info["id_value"] or "",
				"mobile": "",
			},
			"payments": [{
				"type": payment_type.lower(),
				"amount": round(total_amount, 2),
			}],
			"items": items,
		}

		return payload
