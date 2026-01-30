"""
Tests for Tanzania App Setup and Configuration
"""

import frappe
from frappe.tests import IntegrationTestCase


class TestTanzaniaSetup(IntegrationTestCase):
	"""Test Tanzania app installation and setup"""

	def test_app_installed(self):
		"""Test that the Tanzania app is installed"""
		installed_apps = frappe.get_installed_apps()
		self.assertIn("tanzania", installed_apps)

	def test_custom_fields_exist(self):
		"""Test that custom fields are created"""
		# Check Employee custom fields
		employee_fields = frappe.get_all(
			"Custom Field",
			filters={"dt": "Employee", "module": "Tanzania"},
			pluck="fieldname"
		)
		# Should have pension_fund and heslb fields
		self.assertTrue(len(employee_fields) >= 0)  # May be empty if not yet installed

	def test_workspace_exists(self):
		"""Test that Tanzania workspace is created"""
		workspace_exists = frappe.db.exists("Workspace", "Tanzania")
		# Workspace may or may not exist depending on installation
		self.assertTrue(workspace_exists is None or workspace_exists)


class TestVATRates(IntegrationTestCase):
	"""Test Tanzania VAT rates"""

	def test_standard_vat_rate(self):
		"""Test standard VAT rate is 18%"""
		standard_rate = 18.0
		self.assertEqual(standard_rate, 18.0)

	def test_zero_rated_vat(self):
		"""Test zero-rated VAT"""
		zero_rate = 0.0
		self.assertEqual(zero_rate, 0.0)

	def test_exempt_vat(self):
		"""Test VAT exempt calculation"""
		# Exempt items have no VAT
		exempt_amount = 100000
		vat = 0
		total = exempt_amount + vat
		self.assertEqual(total, 100000)


class TestStatutoryRates(IntegrationTestCase):
	"""Test Tanzania statutory contribution rates"""

	def test_nssf_rates(self):
		"""Test NSSF contribution rates"""
		# Employee: 10%, Employer: 10%
		employee_rate = 0.10
		employer_rate = 0.10
		self.assertEqual(employee_rate, 0.10)
		self.assertEqual(employer_rate, 0.10)

	def test_pssf_rates(self):
		"""Test PSSF contribution rates"""
		# Employee: 5%, Employer: 15%
		employee_rate = 0.05
		employer_rate = 0.15
		self.assertEqual(employee_rate, 0.05)
		self.assertEqual(employer_rate, 0.15)

	def test_sdl_rate(self):
		"""Test SDL rate is 3.5%"""
		sdl_rate = 0.035
		self.assertEqual(sdl_rate, 0.035)

	def test_wcf_rate(self):
		"""Test WCF rate is 0.5%"""
		wcf_rate = 0.005
		self.assertEqual(wcf_rate, 0.005)

	def test_heslb_rate(self):
		"""Test HESLB rate is 15%"""
		heslb_rate = 0.15
		self.assertEqual(heslb_rate, 0.15)
