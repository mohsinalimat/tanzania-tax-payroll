"""
Tanzania VAT Summary Report
Shows Output VAT and Input VAT summary for tax compliance
"""

import frappe
from frappe import _


def execute(filters=None):
	return VATSummaryReport(filters).run()


class VATSummaryReport:
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
				"fieldname": "vrn",
				"label": _("VRN"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "net_amount",
				"label": _("Net Amount"),
				"fieldtype": "Currency",
				"width": 120
			},
			{
				"fieldname": "vat_amount",
				"label": _("VAT Amount"),
				"fieldtype": "Currency",
				"width": 120
			},
			{
				"fieldname": "grand_total",
				"label": _("Grand Total"),
				"fieldtype": "Currency",
				"width": 120
			},
			{
				"fieldname": "vat_rate",
				"label": _("VAT Rate %"),
				"fieldtype": "Percent",
				"width": 100
			},
		]

	def get_data(self):
		"""Get report data"""
		self.data = []
		
		# Get Sales Invoices (Output VAT)
		if not self.filters.get("voucher_type") or self.filters.voucher_type == "Sales Invoice":
			sales_data = frappe.db.sql("""
				SELECT 
					si.posting_date,
					'Sales Invoice' as voucher_type,
					si.name as voucher_no,
					si.customer as party,
					c.customer_name as party_name,
					c.vrn,
					si.base_net_total as net_amount,
					si.base_total_taxes_and_charges as vat_amount,
					si.base_grand_total as grand_total,
					COALESCE((
						SELECT AVG(rate) 
						FROM `tabSales Taxes and Charges` 
						WHERE parent = si.name AND account_head LIKE '%%Output VAT%%'
					), 0) as vat_rate
				FROM `tabSales Invoice` si
				LEFT JOIN `tabCustomer` c ON si.customer = c.name
				WHERE si.docstatus = 1
					AND si.is_opening = 'No'
					AND si.company = %(company)s
					AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
				ORDER BY si.posting_date, si.name
			""", self.filters, as_dict=1)
			self.data.extend(sales_data)

		# Get Purchase Invoices (Input VAT)
		if not self.filters.get("voucher_type") or self.filters.voucher_type == "Purchase Invoice":
			purchase_data = frappe.db.sql("""
				SELECT 
					pi.posting_date,
					'Purchase Invoice' as voucher_type,
					pi.name as voucher_no,
					pi.supplier as party,
					s.supplier_name as party_name,
					s.vrn,
					pi.base_net_total as net_amount,
					pi.base_total_taxes_and_charges as vat_amount,
					pi.base_grand_total as grand_total,
					COALESCE((
						SELECT AVG(rate) 
						FROM `tabPurchase Taxes and Charges` 
						WHERE parent = pi.name AND account_head LIKE '%%Input VAT%%'
					), 0) as vat_rate
				FROM `tabPurchase Invoice` pi
				LEFT JOIN `tabSupplier` s ON pi.supplier = s.name
				WHERE pi.docstatus = 1
					AND pi.is_opening = 'No'
					AND pi.company = %(company)s
					AND pi.posting_date BETWEEN %(from_date)s AND %(to_date)s
				ORDER BY pi.posting_date, pi.name
			""", self.filters, as_dict=1)
			self.data.extend(purchase_data)
