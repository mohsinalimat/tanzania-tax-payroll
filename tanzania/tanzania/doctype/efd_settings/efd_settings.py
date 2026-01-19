"""
EFD Settings DocType Controller
Handles TRA EFD device configuration and registration
"""

import frappe
from frappe import _
from frappe.model.document import Document
import requests
import json


class EFDSettings(Document):
	def validate(self):
		if self.enabled and not self.api_key:
			frappe.throw(_("API Key is required when EFD is enabled"))

	def on_update(self):
		if self.enabled and self.api_key:
			self.fetch_device_info()

	@frappe.whitelist()
	def fetch_device_info(self):
		"""Fetch device information from TRA via provider API"""
		if not self.api_key:
			frappe.throw(_("API Key is required"))

		try:
			provider = get_efd_provider(self.provider)
			response = provider.get_device_info(self)

			if response.get("success"):
				data = response.get("data", {})
				self.db_set("tin", data.get("tin", ""))
				self.db_set("vrn", data.get("vrn", ""))
				self.db_set("device_serial", data.get("serial", ""))
				self.db_set("company_name", data.get("company_name", ""))
				self.db_set("address", data.get("address", ""))
				self.db_set("city", data.get("city", ""))
				self.db_set("region", data.get("region", ""))
				self.db_set("tax_office", data.get("tax_office", ""))
				self.db_set("registration_id", data.get("registration_id", ""))
				self.db_set("registration_date", data.get("registration_date"))
				self.db_set("expiry_date", data.get("expiry_date"))
				self.db_set("gc_counter", data.get("gc", 0))
				self.db_set("last_response", json.dumps(response, indent=2))

				frappe.msgprint(_("Device info fetched successfully"))
			else:
				self.db_set("last_response", json.dumps(response, indent=2))
				frappe.throw(_("Failed to fetch device info: {0}").format(response.get("message", "Unknown error")))

		except Exception as e:
			frappe.log_error(str(e), "EFD Device Info Fetch Error")
			frappe.throw(_("Error fetching device info: {0}").format(str(e)))

	@frappe.whitelist()
	def test_connection(self):
		"""Test connection to EFD provider"""
		if not self.api_key:
			frappe.throw(_("API Key is required"))

		try:
			provider = get_efd_provider(self.provider)
			response = provider.test_connection(self)

			if response.get("success"):
				frappe.msgprint(_("Connection successful!"))
			else:
				frappe.throw(_("Connection failed: {0}").format(response.get("message", "Unknown error")))

		except Exception as e:
			frappe.log_error(str(e), "EFD Connection Test Error")
			frappe.throw(_("Connection error: {0}").format(str(e)))


def get_efd_settings(company):
	"""Get EFD Settings for a company"""
	if frappe.db.exists("EFD Settings", company):
		return frappe.get_doc("EFD Settings", company)
	return None


def get_efd_provider(provider_name):
	"""Get EFD provider class instance"""
	from tanzania.efd.providers import get_provider
	return get_provider(provider_name)
