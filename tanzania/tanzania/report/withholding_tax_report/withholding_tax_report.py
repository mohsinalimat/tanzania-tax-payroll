"""
Tanzania Withholding Tax Report
Shows withholding tax details for compliance
"""

import frappe
from frappe import _


def execute(filters=None):
	return WithholdingTaxReport(filters).run()


class WithholdingTaxReport:
	def __init__(self, filters=None):
		self.filters = frappe._dict(filters or {})
		self.columns = []
		self.data = []

	def run(self):
		self.get_columns()
		self.get_data()
		return self.columns, self.data

	def get_columns(self):
		"""Define report columns"""
		self.columns = [
			{
				"fieldname": "posting_date",
				"label": _("Date"),
				"fieldtype": "Date",
				"width": 100
			},
			{
				"fieldname": "voucher_type",
				"label": _("Voucher Type"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "voucher_no",
				"label": _("Voucher No"),
				"fieldtype": "Dynamic Link",
				"options": "voucher_type",
				"width": 150
			},
			{
				"fieldname": "party",
				"label": _("Party"),
				"fieldtype": "Data",
				"width": 150
			},
			{
				"fieldname": "party_name",
				"label": _("Party Name"),
				"fieldtype": "Data",
				"width": 200
			},
			{
				"fieldname": "tin",
				"label": _("TIN"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "base_amount",
				"label": _("Base Amount"),
				"fieldtype": "Currency",
				"width": 120
			},
			{
				"fieldname": "withholding_tax_rate",
				"label": _("WHT Rate %"),
				"fieldtype": "Percent",
				"width": 100
			},
			{
				"fieldname": "withholding_tax_amount",
				"label": _("Withholding Tax Amount"),
				"fieldtype": "Currency",
				"width": 150
			},
		]

	def get_data(self):
		"""Get withholding tax data"""
		conditions = self.get_conditions()
		
		# Get Withholding Tax from Sales Invoices (on customers)
		sales_data = frappe.db.sql("""
			SELECT 
				si.posting_date,
				'Sales Invoice' as voucher_type,
				si.name as voucher_no,
				si.customer as party,
				c.customer_name as party_name,
				c.tin,
				si.base_net_total as base_amount,
				COALESCE((
					SELECT rate 
					FROM `tabSales Taxes and Charges` 
					WHERE parent = si.name 
						AND account_head LIKE '%%Withholding Tax%%'
					LIMIT 1
				), 0) as withholding_tax_rate,
				COALESCE((
					SELECT base_tax_amount 
					FROM `tabSales Taxes and Charges` 
					WHERE parent = si.name 
						AND account_head LIKE '%%Withholding Tax%%'
					LIMIT 1
				), 0) as withholding_tax_amount
			FROM `tabSales Invoice` si
			LEFT JOIN `tabCustomer` c ON si.customer = c.name
			WHERE si.docstatus = 1
				AND si.is_opening = 'No'
				AND si.company = %(company)s
				AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
				AND EXISTS (
					SELECT 1 FROM `tabSales Taxes and Charges` stc
					WHERE stc.parent = si.name
						AND stc.account_head LIKE '%%Withholding Tax%%'
				)
				""" + conditions + """
			ORDER BY si.posting_date, si.name
		""", self.filters, as_dict=1)  # nosemgrep: frappe-sql-format-injection

		# Get Withholding Tax from Purchase Invoices (on suppliers)
		purchase_data = frappe.db.sql("""
			SELECT 
				pi.posting_date,
				'Purchase Invoice' as voucher_type,
				pi.name as voucher_no,
				pi.supplier as party,
				s.supplier_name as party_name,
				s.tin,
				pi.base_net_total as base_amount,
				COALESCE((
					SELECT rate 
					FROM `tabPurchase Taxes and Charges` 
					WHERE parent = pi.name 
						AND account_head LIKE '%%Withholding Tax%%'
					LIMIT 1
				), 0) as withholding_tax_rate,
				COALESCE((
					SELECT base_tax_amount 
					FROM `tabPurchase Taxes and Charges` 
					WHERE parent = pi.name 
						AND account_head LIKE '%%Withholding Tax%%'
					LIMIT 1
				), 0) as withholding_tax_amount
			FROM `tabPurchase Invoice` pi
			LEFT JOIN `tabSupplier` s ON pi.supplier = s.name
			WHERE pi.docstatus = 1
				AND pi.is_opening = 'No'
				AND pi.company = %(company)s
				AND pi.posting_date BETWEEN %(from_date)s AND %(to_date)s
				AND EXISTS (
					SELECT 1 FROM `tabPurchase Taxes and Charges` ptc
					WHERE ptc.parent = pi.name
						AND ptc.account_head LIKE '%%Withholding Tax%%'
				)
				""" + conditions + """
			ORDER BY pi.posting_date, pi.name
		""", self.filters, as_dict=1)  # nosemgrep: frappe-sql-format-injection

		self.data = sales_data + purchase_data

	def get_conditions(self):
		"""Build filter conditions"""
		return ""
