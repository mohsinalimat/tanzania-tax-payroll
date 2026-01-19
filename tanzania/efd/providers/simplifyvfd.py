"""
SimplifyVFD EFD Provider
Integration with SimplifyVFD API for TRA fiscal receipts
"""

import frappe
from frappe import _
from tanzania.efd.providers.base import BaseEFDProvider


# SimplifyVFD-specific ID type mapping
SIMPLIFY_ID_TYPES = {
	"1": "TAX_IDENTIFICATION_NUMBER",
	"2": "DRIVING_LICENCE",
	"3": "VOTERS_NUMBER",
	"4": "TRAVEL_DOCUMENT",
	"5": "NATIONAL_ID",
	"6": "NIL",
}

# SimplifyVFD-specific tax type mapping
SIMPLIFY_TAX_TYPES = {
	"A": "STANDARD",
	"B": "SPECIAL_RATE",
	"C": "ZERO_RATED",
	"D": "SPECIAL_RELIEF",
	"E": "EXEMPTED",
}


class SimplifyVFDProvider(BaseEFDProvider):
	"""SimplifyVFD EFD Provider implementation"""

	name = "SimplifyVFD"
	base_url = "https://api.simplifyvfd.co.tz/api/v1"
	timeout = 120

	def get_headers(self, settings):
		"""Get request headers with bearer token"""
		return {
			"Content-Type": "application/json",
			"Authorization": f"Bearer {settings.get_password('api_key') or ''}",
		}

	def get_device_info(self, settings):
		"""Fetch device information from SimplifyVFD"""
		url = f"{self.base_url}/device/info"
		headers = self.get_headers(settings)

		response = self.make_request(url, method="GET", headers=headers)

		if not response.get("success"):
			return response

		data = response.get("data", {})

		if data.get("success") or data.get("tin"):
			return {
				"success": True,
				"data": {
					"tin": data.get("tin", ""),
					"vrn": data.get("vrn", ""),
					"serial": data.get("serialNumber", ""),
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
		"""Post fiscal receipt to SimplifyVFD"""
		url = f"{self.base_url}/invoice"
		headers = self.get_headers(settings)

		response = self.make_request(url, method="POST", headers=headers, data=payload)

		if not response.get("success"):
			return response

		data = response.get("data", {})

		if data.get("success"):
			verification_code = data.get("verificationCode", "")
			verification_url = data.get("verificationUrl", "")
			issued_at = data.get("issuedAt", "")

			# Parse date and time from issuedAt
			date_str = ""
			time_str = ""
			if issued_at:
				parts = issued_at.split("T")
				date_str = parts[0] if parts else ""
				time_str = parts[1][:8] if len(parts) > 1 else ""

			return {
				"success": True,
				"data": {
					"receipt_number": verification_code,
					"verification_code": verification_code,
					"verification_url": verification_url,
					"date": date_str,
					"time": time_str,
					"invoice_id": data.get("invoiceId", ""),
					"gc": data.get("gc", 0),
					"dc": data.get("dc", 0),
				},
				"message": "Receipt posted successfully"
			}
		else:
			return {
				"success": False,
				"code": data.get("code"),
				"message": data.get("message", "Failed to post receipt"),
				"data": data
			}

	def get_simplify_id_type(self, id_type):
		"""Convert ID type to SimplifyVFD format"""
		return SIMPLIFY_ID_TYPES.get(id_type, "NIL")

	def get_simplify_tax_type(self, tax_code):
		"""Convert tax code to SimplifyVFD format"""
		return SIMPLIFY_TAX_TYPES.get(tax_code, "STANDARD")

	def build_payload(self, settings, invoice_doc):
		"""Build receipt payload for SimplifyVFD"""
		# Get customer info
		customer_info = self.get_customer_info(invoice_doc.customer)

		# Format date
		date_str, _ = self.format_datetime(invoice_doc.posting_date)

		# Build items
		items = []
		for item in invoice_doc.items:
			tax_info = self.get_item_tax_code(item.item_code, item.item_tax_template)
			tax_type = self.get_simplify_tax_type(tax_info["code"])

			# Calculate amount
			amount = self.calculate_item_amount(item, tax_info["rate"], is_inclusive=True)
			unit_price = amount / item.qty if item.qty else amount

			items.append({
				"description": f"{item.item_code} - {item.item_name or ''}",
				"quantity": item.qty,
				"unitAmount": round(unit_price, 2),
				"discountRate": 0.0,
				"taxType": tax_type,
			})

		# Get payment type
		payment_type = self.get_payment_type(invoice_doc.get("mode_of_payment"))

		# Calculate totals
		total_amount = invoice_doc.grand_total or invoice_doc.rounded_total or 0

		# Convert ID type to SimplifyVFD format
		id_type = self.get_simplify_id_type(customer_info["id_type"])

		payload = {
			"dateTime": date_str,
			"customer": {
				"identificationType": id_type,
				"identificationNumber": customer_info["id_value"] or "",
				"vatRegistrationNumber": customer_info["vrn"] or "",
				"name": customer_info["name"],
				"mobileNumber": "",
				"email": "",
			},
			"invoiceAmountType": "INCLUSIVE",
			"items": items,
			"payments": [{
				"type": payment_type,
				"amount": round(total_amount, 2),
			}],
			"partnerInvoiceId": invoice_doc.name,
		}

		return payload
