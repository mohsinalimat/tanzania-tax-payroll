"""
Base EFD Provider Class
Abstract base class for all EFD provider implementations
"""

import frappe
from frappe import _
import requests
import json
from abc import ABC, abstractmethod
from time import sleep


# Tax code mapping (TRA standard)
TAX_CODES = {
	"A-Standard 18%": {"code": "A", "id": "1", "rate": 18.0},
	"B-Special Rate": {"code": "B", "id": "2", "rate": 0.0},
	"C-Zero Rated": {"code": "C", "id": "3", "rate": 0.0},
	"D-Special Relief": {"code": "D", "id": "4", "rate": 0.0},
	"E-Exempt": {"code": "E", "id": "5", "rate": 0.0},
	# Legacy numeric codes
	"1": {"code": "A", "id": "1", "rate": 18.0},
	"2": {"code": "B", "id": "2", "rate": 0.0},
	"3": {"code": "C", "id": "3", "rate": 0.0},
	"4": {"code": "D", "id": "4", "rate": 0.0},
	"5": {"code": "E", "id": "5", "rate": 0.0},
}

# Customer ID type mapping
CUSTOMER_ID_TYPES = {
	"1-TIN": "1",
	"2-Driving License": "2",
	"3-Voter ID": "3",
	"4-Passport": "4",
	"5-NID": "5",
	"6-Other": "6",
}

# Payment type mapping
PAYMENT_TYPES = {
	"CASH": "CASH",
	"CHEQUE": "CHEQUE",
	"CCARD": "CCARD",
	"EMONEY": "EMONEY",
	"INVOICE": "INVOICE",
}


class BaseEFDProvider(ABC):
	"""Abstract base class for EFD providers"""

	name = "Base"
	base_url = ""
	timeout = 60
	max_retries = 3

	@abstractmethod
	def get_device_info(self, settings):
		"""Fetch device information from TRA

		Args:
			settings: EFD Settings document

		Returns:
			dict: {success: bool, data: dict, message: str}
		"""
		pass

	@abstractmethod
	def post_receipt(self, settings, invoice_doc, payload):
		"""Post fiscal receipt to TRA

		Args:
			settings: EFD Settings document
			invoice_doc: Sales Invoice document
			payload: Receipt payload

		Returns:
			dict: {success: bool, data: dict, message: str}
		"""
		pass

	@abstractmethod
	def build_payload(self, settings, invoice_doc):
		"""Build receipt payload from invoice

		Args:
			settings: EFD Settings document
			invoice_doc: Sales Invoice document

		Returns:
			dict: Receipt payload
		"""
		pass

	def test_connection(self, settings):
		"""Test connection to provider API

		Args:
			settings: EFD Settings document

		Returns:
			dict: {success: bool, message: str}
		"""
		return self.get_device_info(settings)

	def make_request(self, url, method="GET", headers=None, data=None, timeout=None):
		"""Make HTTP request with retry logic

		Args:
			url: Request URL
			method: HTTP method (GET, POST)
			headers: Request headers
			data: Request payload
			timeout: Request timeout

		Returns:
			dict: Response data or error
		"""
		timeout = timeout or self.timeout
		headers = headers or {}
		last_error = None

		for attempt in range(self.max_retries):
			try:
				if method.upper() == "GET":
					response = requests.get(url, headers=headers, timeout=timeout)
				elif method.upper() == "POST":
					response = requests.post(
						url,
						headers=headers,
						json=data,
						timeout=timeout
					)
				else:
					raise ValueError(f"Unsupported HTTP method: {method}")

				response.raise_for_status()
				return {
					"success": True,
					"status_code": response.status_code,
					"data": response.json() if response.content else {}
				}

			except requests.exceptions.Timeout:
				last_error = "Request timed out"
			except requests.exceptions.ConnectionError:
				last_error = "Connection error"
			except requests.exceptions.HTTPError as e:
				# Try to get error message from response body
				try:
					error_data = e.response.json()
					last_error = error_data.get("message", f"HTTP error: {e.response.status_code}")
				except Exception:
					last_error = f"HTTP error: {e.response.status_code}"
				# Don't retry on client errors (4xx)
				if e.response.status_code < 500:
					break
			except json.JSONDecodeError:
				last_error = "Invalid JSON response"
			except Exception as e:
				last_error = str(e)

			# Wait before retry (exponential backoff)
			if attempt < self.max_retries - 1:
				sleep(2 ** attempt)

		return {
			"success": False,
			"message": last_error or "Unknown error"
		}

	def get_tax_info(self, efd_tax_code):
		"""Get tax code info from EFD tax code

		Args:
			efd_tax_code: Tax code from Item Tax Template (e.g., "A-Standard 18%")

		Returns:
			dict: {code: str, id: str, rate: float}
		"""
		if not efd_tax_code:
			# Default to Standard 18%
			return TAX_CODES["A-Standard 18%"]
		return TAX_CODES.get(efd_tax_code, TAX_CODES["A-Standard 18%"])

	def get_customer_id_type(self, id_type):
		"""Get customer ID type code

		Args:
			id_type: ID type from Customer (e.g., "1-TIN")

		Returns:
			str: ID type code (e.g., "1")
		"""
		if not id_type:
			return "6"  # Default to Other
		return CUSTOMER_ID_TYPES.get(id_type, "6")

	def get_payment_type(self, mode_of_payment):
		"""Get payment type from Mode of Payment

		Args:
			mode_of_payment: Mode of Payment name

		Returns:
			str: Payment type code
		"""
		if not mode_of_payment:
			return "INVOICE"

		# Try to get EFD payment type from Mode of Payment
		efd_type = frappe.db.get_value(
			"Mode of Payment",
			mode_of_payment,
			"efd_payment_type"
		)
		return efd_type or "INVOICE"

	def get_item_tax_code(self, item_code, item_tax_template=None):
		"""Get EFD tax code for an item

		Args:
			item_code: Item code
			item_tax_template: Item Tax Template name (optional)

		Returns:
			dict: Tax info {code, id, rate}
		"""
		efd_tax_code = None

		# First try item tax template
		if item_tax_template:
			efd_tax_code = frappe.db.get_value(
				"Item Tax Template",
				item_tax_template,
				"efd_tax_code"
			)

		# If not found, try item's default tax template
		if not efd_tax_code:
			item_tax_template = frappe.db.get_value("Item", item_code, "item_tax_template")
			if item_tax_template:
				efd_tax_code = frappe.db.get_value(
					"Item Tax Template",
					item_tax_template,
					"efd_tax_code"
				)

		return self.get_tax_info(efd_tax_code)

	def get_customer_info(self, customer_name):
		"""Get customer info for EFD receipt

		Args:
			customer_name: Customer name

		Returns:
			dict: {name, id_type, id_value, vrn}
		"""
		customer = frappe.get_doc("Customer", customer_name)

		id_type = self.get_customer_id_type(customer.get("efd_id_type"))
		id_value = customer.get("tin") or ""

		# Auto-set ID type based on TIN presence
		if id_value and id_type == "6":
			id_type = "1"  # TIN

		return {
			"name": customer.customer_name,
			"id_type": id_type,
			"id_value": id_value,
			"vrn": customer.get("vrn") or "",
		}

	def calculate_item_amount(self, item, tax_rate, is_inclusive=True):
		"""Calculate item amount for EFD

		Args:
			item: Invoice item
			tax_rate: Tax rate (e.g., 18.0)
			is_inclusive: Whether prices are tax-inclusive

		Returns:
			float: Item amount
		"""
		base_amount = item.get("base_amount") or item.get("amount") or 0

		if is_inclusive:
			return base_amount
		else:
			# Add tax for exclusive prices
			if tax_rate > 0:
				return base_amount * (1 + tax_rate / 100)
			return base_amount

	def format_datetime(self, date, time=None):
		"""Format date and time for EFD

		Args:
			date: Date value
			time: Time value (optional)

		Returns:
			tuple: (date_str, time_str)
		"""
		from frappe.utils import today, nowtime, getdate, get_time

		date_str = str(getdate(date) if date else today())
		time_str = str(get_time(time) if time else nowtime())[:8]

		return date_str, time_str

	def generate_verification_url(self, receipt_number, time_str):
		"""Generate TRA verification URL

		Args:
			receipt_number: Receipt number from TRA
			time_str: Receipt time

		Returns:
			str: Verification URL
		"""
		if not receipt_number:
			return ""
		# Remove colons from time
		time_clean = time_str.replace(":", "") if time_str else ""
		return f"https://verify.tra.go.tz/{receipt_number}_{time_clean}"

	def log_error(self, title, message, reference=None):
		"""Log error to Error Log

		Args:
			title: Error title
			message: Error message
			reference: Reference document (optional)
		"""
		frappe.log_error(
			title=f"EFD {self.name}: {title}",
			message=f"Reference: {reference}\n\n{message}" if reference else message
		)
