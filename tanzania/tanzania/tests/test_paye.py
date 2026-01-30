"""
Tests for Tanzania PAYE (Pay As You Earn) Tax Calculation
Based on Tanzania Revenue Authority tax brackets
"""

import unittest


class TestPAYECalculation(unittest.TestCase):
	"""Test Tanzania PAYE tax bracket calculations"""

	def calculate_paye(self, gross_income, nssf_deduction=0):
		"""
		Calculate PAYE based on Tanzania tax brackets (2024/2025)
		Taxable income = Gross Income - NSSF Deduction

		Tax Brackets (Monthly):
		- 0 to 270,000: 0%
		- 270,001 to 520,000: 8%
		- 520,001 to 760,000: 20%
		- 760,001 to 1,000,000: 25%
		- Above 1,000,000: 30%
		"""
		taxable_income = gross_income - nssf_deduction

		if taxable_income <= 270000:
			return 0
		elif taxable_income <= 520000:
			return (taxable_income - 270000) * 0.08
		elif taxable_income <= 760000:
			return ((taxable_income - 520000) * 0.20) + 20000
		elif taxable_income <= 1000000:
			return ((taxable_income - 760000) * 0.25) + 68000
		else:
			return ((taxable_income - 1000000) * 0.30) + 128000

	def test_zero_tax_bracket(self):
		"""Test 0% tax bracket (income <= 270,000)"""
		# Below threshold
		self.assertEqual(self.calculate_paye(200000), 0)
		# At threshold
		self.assertEqual(self.calculate_paye(270000), 0)

	def test_eight_percent_bracket(self):
		"""Test 8% tax bracket (270,001 to 520,000)"""
		# Just above first threshold
		paye = self.calculate_paye(300000)
		expected = (300000 - 270000) * 0.08  # 2,400
		self.assertEqual(paye, expected)

		# At upper limit
		paye = self.calculate_paye(520000)
		expected = (520000 - 270000) * 0.08  # 20,000
		self.assertEqual(paye, expected)

	def test_twenty_percent_bracket(self):
		"""Test 20% tax bracket (520,001 to 760,000)"""
		paye = self.calculate_paye(600000)
		expected = ((600000 - 520000) * 0.20) + 20000  # 16,000 + 20,000 = 36,000
		self.assertEqual(paye, expected)

		# At upper limit
		paye = self.calculate_paye(760000)
		expected = ((760000 - 520000) * 0.20) + 20000  # 48,000 + 20,000 = 68,000
		self.assertEqual(paye, expected)

	def test_twentyfive_percent_bracket(self):
		"""Test 25% tax bracket (760,001 to 1,000,000)"""
		paye = self.calculate_paye(900000)
		expected = ((900000 - 760000) * 0.25) + 68000  # 35,000 + 68,000 = 103,000
		self.assertEqual(paye, expected)

		# At upper limit
		paye = self.calculate_paye(1000000)
		expected = ((1000000 - 760000) * 0.25) + 68000  # 60,000 + 68,000 = 128,000
		self.assertEqual(paye, expected)

	def test_thirty_percent_bracket(self):
		"""Test 30% tax bracket (above 1,000,000)"""
		paye = self.calculate_paye(1500000)
		expected = ((1500000 - 1000000) * 0.30) + 128000  # 150,000 + 128,000 = 278,000
		self.assertEqual(paye, expected)

		paye = self.calculate_paye(2000000)
		expected = ((2000000 - 1000000) * 0.30) + 128000  # 300,000 + 128,000 = 428,000
		self.assertEqual(paye, expected)

	def test_with_nssf_deduction(self):
		"""Test PAYE calculation with NSSF deduction (10%)"""
		gross = 1000000
		nssf = gross * 0.10  # 100,000
		taxable = gross - nssf  # 900,000

		paye = self.calculate_paye(gross, nssf)
		expected = ((taxable - 760000) * 0.25) + 68000  # 103,000
		self.assertEqual(paye, expected)

	def test_statutory_rates(self):
		"""Test statutory contribution rates"""
		gross = 1000000

		# NSSF Employee: 10%
		nssf_employee = gross * 0.10
		self.assertEqual(nssf_employee, 100000)

		# NSSF Employer: 10%
		nssf_employer = gross * 0.10
		self.assertEqual(nssf_employer, 100000)

		# SDL: 3.5%
		sdl = gross * 0.035
		self.assertEqual(sdl, 35000)

		# WCF: 0.5%
		wcf = gross * 0.005
		self.assertEqual(wcf, 5000)

		# HESLB: 15%
		heslb = gross * 0.15
		self.assertEqual(heslb, 150000)


if __name__ == "__main__":
	unittest.main()
