"""
Tanzania VAT Return Report
Comprehensive VAT return report for TRA (Tanzania Revenue Authority) filing
"""

import frappe
from frappe import _


def execute(filters=None):
	return VATReturnReport(filters).run()


class VATReturnReport:
	def __init__(self, filters=None):
		self.filters = frappe._dict(filters or {})
		self.columns = []
		self.data = []

	def run(self):
		self.get_columns()
		self.get_data()
		return self.columns, self.data

	def get_columns(self):
		"""Define report columns for VAT Return"""
		self.columns = [
			{
				"fieldname": "section",
				"label": _("Section"),
				"fieldtype": "Data",
				"width": 200
			},
			{
				"fieldname": "description",
				"label": _("Description"),
				"fieldtype": "Data",
				"width": 300
			},
			{
				"fieldname": "amount",
				"label": _("Amount"),
				"fieldtype": "Currency",
				"width": 150
			},
		]

	def get_data(self):
		"""Get VAT return data organized by sections"""
		self.data = []
		
		# Section 1: Output VAT (Sales)
		output_vat = self.get_output_vat()
		self.data.append({
			"section": "OUTPUT VAT",
			"description": "Total VAT on Sales (Standard Rated)",
			"amount": output_vat.get("standard_rated", 0)
		})
		self.data.append({
			"section": "",
			"description": "Total VAT on Sales (Zero Rated)",
			"amount": output_vat.get("zero_rated", 0)
		})
		self.data.append({
			"section": "",
			"description": "Total VAT on Sales (Exempt)",
			"amount": output_vat.get("exempt", 0)
		})
		self.data.append({
			"section": "",
			"description": "Total Output VAT",
			"amount": output_vat.get("total", 0),
			"indent": 0,
			"bold": 1
		})
		
		# Section 2: Input VAT (Purchases)
		input_vat = self.get_input_vat()
		self.data.append({
			"section": "INPUT VAT",
			"description": "Total VAT on Purchases (Standard Rated)",
			"amount": input_vat.get("standard_rated", 0)
		})
		self.data.append({
			"section": "",
			"description": "Total VAT on Purchases (Zero Rated)",
			"amount": input_vat.get("zero_rated", 0)
		})
		self.data.append({
			"section": "",
			"description": "Total VAT on Purchases (Exempt)",
			"amount": input_vat.get("exempt", 0)
		})
		self.data.append({
			"section": "",
			"description": "Total Input VAT",
			"amount": input_vat.get("total", 0),
			"indent": 0,
			"bold": 1
		})
		
		# Section 3: Net VAT Payable
		net_vat = output_vat.get("total", 0) - input_vat.get("total", 0)
		self.data.append({
			"section": "NET VAT PAYABLE",
			"description": "VAT Payable to TRA",
			"amount": net_vat if net_vat > 0 else 0,
			"indent": 0,
			"bold": 1
		})
		
		# Section 4: VAT Refundable
		if net_vat < 0:
			self.data.append({
				"section": "VAT REFUNDABLE",
				"description": "VAT Refundable from TRA",
				"amount": abs(net_vat),
				"indent": 0,
				"bold": 1
			})

	def get_output_vat(self):
		"""Calculate Output VAT from Sales Invoices"""
		result = frappe.db.sql("""
			SELECT 
				COALESCE(SUM(CASE WHEN stc.rate > 0 THEN stc.base_tax_amount ELSE 0 END), 0) as standard_rated,
				COALESCE(SUM(CASE WHEN stc.rate = 0 AND si.tax_category = 'Zero Rated' THEN si.base_net_total ELSE 0 END), 0) as zero_rated,
				COALESCE(SUM(CASE WHEN si.tax_category = 'Exempt' THEN si.base_net_total ELSE 0 END), 0) as exempt,
				COALESCE(SUM(stc.base_tax_amount), 0) as total
			FROM `tabSales Invoice` si
			LEFT JOIN `tabSales Taxes and Charges` stc ON si.name = stc.parent
				AND stc.account_head LIKE '%%Output VAT%%'
			WHERE si.docstatus = 1
				AND si.is_opening = 'No'
				AND si.company = %(company)s
				AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
		""", self.filters, as_dict=1)
		
		return result[0] if result else {"standard_rated": 0, "zero_rated": 0, "exempt": 0, "total": 0}

	def get_input_vat(self):
		"""Calculate Input VAT from Purchase Invoices"""
		result = frappe.db.sql("""
			SELECT 
				COALESCE(SUM(CASE WHEN ptc.rate > 0 THEN ptc.base_tax_amount ELSE 0 END), 0) as standard_rated,
				COALESCE(SUM(CASE WHEN ptc.rate = 0 AND pi.tax_category = 'Zero Rated' THEN pi.base_net_total ELSE 0 END), 0) as zero_rated,
				COALESCE(SUM(CASE WHEN pi.tax_category = 'Exempt' THEN pi.base_net_total ELSE 0 END), 0) as exempt,
				COALESCE(SUM(ptc.base_tax_amount), 0) as total
			FROM `tabPurchase Invoice` pi
			LEFT JOIN `tabPurchase Taxes and Charges` ptc ON pi.name = ptc.parent
				AND ptc.account_head LIKE '%%Input VAT%%'
			WHERE pi.docstatus = 1
				AND pi.is_opening = 'No'
				AND pi.company = %(company)s
				AND pi.posting_date BETWEEN %(from_date)s AND %(to_date)s
		""", self.filters, as_dict=1)
		
		return result[0] if result else {"standard_rated": 0, "zero_rated": 0, "exempt": 0, "total": 0}
