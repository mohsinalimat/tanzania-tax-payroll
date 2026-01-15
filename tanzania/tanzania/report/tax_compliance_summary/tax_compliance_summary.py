"""
Tanzania Tax Compliance Summary Report
Comprehensive summary of all tax obligations and compliance status
"""

import frappe
from frappe import _


def execute(filters=None):
	return TaxComplianceSummary(filters).run()


class TaxComplianceSummary:
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
				"fieldname": "tax_type",
				"label": _("Tax Type"),
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
			{
				"fieldname": "status",
				"label": _("Status"),
				"fieldtype": "Data",
				"width": 120
			},
		]

	def get_data(self):
		"""Get tax compliance summary data"""
		self.data = []
		
		# VAT Summary
		vat_summary = self.get_vat_summary()
		self.data.append({
			"tax_type": "VAT",
			"description": "Output VAT (Sales)",
			"amount": vat_summary.get("output_vat", 0),
			"status": "Payable"
		})
		self.data.append({
			"tax_type": "",
			"description": "Input VAT (Purchases)",
			"amount": vat_summary.get("input_vat", 0),
			"status": "Creditable"
		})
		self.data.append({
			"tax_type": "",
			"description": "Net VAT Payable",
			"amount": vat_summary.get("net_vat", 0),
			"status": "Payable" if vat_summary.get("net_vat", 0) > 0 else "Refundable",
			"bold": 1
		})
		
		# Withholding Tax Summary
		wht_summary = self.get_withholding_tax_summary()
		self.data.append({
			"tax_type": "WITHHOLDING TAX",
			"description": "Withholding Tax on Sales",
			"amount": wht_summary.get("on_sales", 0),
			"status": "Collected"
		})
		self.data.append({
			"tax_type": "",
			"description": "Withholding Tax on Purchases",
			"amount": wht_summary.get("on_purchases", 0),
			"status": "Paid"
		})
		self.data.append({
			"tax_type": "",
			"description": "Net Withholding Tax",
			"amount": wht_summary.get("net", 0),
			"status": "Payable" if wht_summary.get("net", 0) > 0 else "Receivable",
			"bold": 1
		})
		
		# PAYE Summary (if payroll is installed)
		if "hrms" in frappe.get_installed_apps():
			paye_summary = self.get_paye_summary()
			if paye_summary.get("total", 0) > 0:
				self.data.append({
					"tax_type": "PAYE",
					"description": "PAYE Payable",
					"amount": paye_summary.get("total", 0),
					"status": "Payable",
					"bold": 1
				})
		
		# SDL Summary (if payroll is installed)
		if "hrms" in frappe.get_installed_apps():
			sdl_summary = self.get_sdl_summary()
			if sdl_summary.get("total", 0) > 0:
				self.data.append({
					"tax_type": "SDL",
					"description": "SDL Payable",
					"amount": sdl_summary.get("total", 0),
					"status": "Payable",
					"bold": 1
				})

	def get_vat_summary(self):
		"""Get VAT summary"""
		result = frappe.db.sql("""
			SELECT 
				COALESCE((
					SELECT SUM(base_tax_amount)
					FROM `tabSales Taxes and Charges` stc
					INNER JOIN `tabSales Invoice` si ON stc.parent = si.name
					WHERE si.docstatus = 1
						AND si.company = %(company)s
						AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
						AND stc.account_head LIKE '%%Output VAT%%'
				), 0) as output_vat,
				COALESCE((
					SELECT SUM(base_tax_amount)
					FROM `tabPurchase Taxes and Charges` ptc
					INNER JOIN `tabPurchase Invoice` pi ON ptc.parent = pi.name
					WHERE pi.docstatus = 1
						AND pi.company = %(company)s
						AND pi.posting_date BETWEEN %(from_date)s AND %(to_date)s
						AND ptc.account_head LIKE '%%Input VAT%%'
				), 0) as input_vat
		""", self.filters, as_dict=1)
		
		if result:
			output_vat = result[0].get("output_vat", 0) or 0
			input_vat = result[0].get("input_vat", 0) or 0
			return {
				"output_vat": output_vat,
				"input_vat": input_vat,
				"net_vat": output_vat - input_vat
			}
		return {"output_vat": 0, "input_vat": 0, "net_vat": 0}

	def get_withholding_tax_summary(self):
		"""Get Withholding Tax summary"""
		result = frappe.db.sql("""
			SELECT 
				COALESCE((
					SELECT SUM(base_tax_amount)
					FROM `tabSales Taxes and Charges` stc
					INNER JOIN `tabSales Invoice` si ON stc.parent = si.name
					WHERE si.docstatus = 1
						AND si.company = %(company)s
						AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
						AND stc.account_head LIKE '%%Withholding Tax%%'
				), 0) as on_sales,
				COALESCE((
					SELECT SUM(base_tax_amount)
					FROM `tabPurchase Taxes and Charges` ptc
					INNER JOIN `tabPurchase Invoice` pi ON ptc.parent = pi.name
					WHERE pi.docstatus = 1
						AND pi.company = %(company)s
						AND pi.posting_date BETWEEN %(from_date)s AND %(to_date)s
						AND ptc.account_head LIKE '%%Withholding Tax%%'
				), 0) as on_purchases
		""", self.filters, as_dict=1)
		
		if result:
			on_sales = result[0].get("on_sales", 0) or 0
			on_purchases = result[0].get("on_purchases", 0) or 0
			return {
				"on_sales": on_sales,
				"on_purchases": on_purchases,
				"net": on_sales - on_purchases
			}
		return {"on_sales": 0, "on_purchases": 0, "net": 0}

	def get_paye_summary(self):
		"""Get PAYE summary from payroll"""
		result = frappe.db.sql("""
			SELECT SUM(amount) as total
			FROM `tabSalary Component` sc
			INNER JOIN `tabSalary Detail` sd ON sc.name = sd.salary_component
			INNER JOIN `tabSalary Slip` ss ON sd.parent = ss.name
			WHERE ss.docstatus = 1
				AND ss.company = %(company)s
				AND ss.posting_date BETWEEN %(from_date)s AND %(to_date)s
				AND sc.name LIKE '%%PAYE%%'
		""", self.filters, as_dict=1)
		
		return {"total": result[0].get("total", 0) or 0} if result else {"total": 0}

	def get_sdl_summary(self):
		"""Get SDL summary from payroll"""
		result = frappe.db.sql("""
			SELECT SUM(amount) as total
			FROM `tabSalary Component` sc
			INNER JOIN `tabSalary Detail` sd ON sc.name = sd.salary_component
			INNER JOIN `tabSalary Slip` ss ON sd.parent = ss.name
			WHERE ss.docstatus = 1
				AND ss.company = %(company)s
				AND ss.posting_date BETWEEN %(from_date)s AND %(to_date)s
				AND sc.name LIKE '%%SDL%%'
		""", self.filters, as_dict=1)
		
		return {"total": result[0].get("total", 0) or 0} if result else {"total": 0}
