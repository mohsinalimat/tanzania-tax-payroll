"""
Tanzania Tax Compliance Custom Fields
Creates TIN and VRN fields for Company, Customer, Supplier, and Invoices
"""

import frappe
from frappe import _
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def get_tanzania_custom_fields():
	"""Returns dictionary of custom fields for Tanzania tax and payroll compliance"""
	return {
		"Employee": [
			{
				"fieldname": "tanzania_payroll_section",
				"fieldtype": "Section Break",
				"label": _("Tanzania Payroll Information"),
				"insert_after": "salary_mode",
			},
			{
				"fieldname": "nssf",
				"fieldtype": "Check",
				"label": _("NSSF Registered"),
				"description": _("Employee is registered with NSSF (National Social Security Fund)"),
				"insert_after": "tanzania_payroll_section",
				"default": 0,
			},
			{
				"fieldname": "pssf",
				"fieldtype": "Check",
				"label": _("PSSF Registered"),
				"description": _("Employee is registered with PSSF (Public Service Social Security Fund)"),
				"insert_after": "nssf",
				"default": 0,
			},
			{
				"fieldname": "column_break_payroll",
				"fieldtype": "Column Break",
				"insert_after": "pssf",
			},
			{
				"fieldname": "heslb",
				"fieldtype": "Check",
				"label": _("HESLB Loan"),
				"description": _("Employee has HESLB (Higher Education Students Loans Board) loan - 15% deduction"),
				"insert_after": "column_break_payroll",
				"default": 0,
			},
			{
				"fieldname": "employment_type",
				"fieldtype": "Select",
				"label": _("Employment Type"),
				"options": "Primary\nSecondary",
				"description": _("Primary or Secondary employment (affects PAYE calculation)"),
				"insert_after": "heslb",
				"default": "Primary",
			},
		],
		"Company": [
			{
				"fieldname": "tanzania_tax_section",
				"fieldtype": "Section Break",
				"label": _("Tanzania Tax Information"),
				"insert_after": "credit_limit",
			},
			{
				"fieldname": "tin",
				"fieldtype": "Data",
				"label": _("TIN (Tax Identification Number)"),
				"description": _("Company Tax Identification Number"),
				"insert_after": "tanzania_tax_section",
			},
			{
				"fieldname": "vrn",
				"fieldtype": "Data",
				"label": _("VRN (VAT Registration Number)"),
				"description": _("Company VAT Registration Number"),
				"insert_after": "tin",
			},
			{
				"fieldname": "column_break_tax_info",
				"fieldtype": "Column Break",
				"insert_after": "vrn",
			},
			{
				"fieldname": "tax_office",
				"fieldtype": "Data",
				"label": _("Tax Office"),
				"description": _("TRA Tax Office"),
				"insert_after": "column_break_tax_info",
			},
		],
		"Customer": [
			{
				"fieldname": "tanzania_tax_section",
				"fieldtype": "Section Break",
				"label": _("Tanzania Tax Information"),
				"insert_after": "credit_limit",
			},
			{
				"fieldname": "tin",
				"fieldtype": "Data",
				"label": _("TIN (Tax Identification Number)"),
				"description": _("Customer Tax Identification Number"),
				"insert_after": "tanzania_tax_section",
			},
			{
				"fieldname": "vrn",
				"fieldtype": "Data",
				"label": _("VRN (VAT Registration Number)"),
				"description": _("Customer VAT Registration Number"),
				"insert_after": "tin",
			},
			{
				"fieldname": "column_break_tax_info",
				"fieldtype": "Column Break",
				"insert_after": "vrn",
			},
			{
				"fieldname": "tax_category",
				"fieldtype": "Link",
				"label": _("Tax Category"),
				"options": "Tax Category",
				"insert_after": "column_break_tax_info",
			},
		],
		"Supplier": [
			{
				"fieldname": "tanzania_tax_section",
				"fieldtype": "Section Break",
				"label": _("Tanzania Tax Information"),
				"insert_after": "credit_limit",
			},
			{
				"fieldname": "tin",
				"fieldtype": "Data",
				"label": _("TIN (Tax Identification Number)"),
				"description": _("Supplier Tax Identification Number"),
				"insert_after": "tanzania_tax_section",
			},
			{
				"fieldname": "vrn",
				"fieldtype": "Data",
				"label": _("VRN (VAT Registration Number)"),
				"description": _("Supplier VAT Registration Number"),
				"insert_after": "tin",
			},
			{
				"fieldname": "column_break_tax_info",
				"fieldtype": "Column Break",
				"insert_after": "vrn",
			},
			{
				"fieldname": "tax_category",
				"fieldtype": "Link",
				"label": _("Tax Category"),
				"options": "Tax Category",
				"insert_after": "column_break_tax_info",
			},
		],
		"Sales Invoice": [
			{
				"fieldname": "tanzania_tax_section",
				"fieldtype": "Section Break",
				"label": _("Tanzania Tax Information"),
				"insert_after": "taxes_section",
			},
			{
				"fieldname": "customer_tin",
				"fieldtype": "Data",
				"label": _("Customer TIN"),
				"fetch_from": "customer.tin",
				"read_only": 1,
				"insert_after": "tanzania_tax_section",
			},
			{
				"fieldname": "customer_vrn",
				"fieldtype": "Data",
				"label": _("Customer VRN"),
				"fetch_from": "customer.vrn",
				"read_only": 1,
				"insert_after": "customer_tin",
			},
			{
				"fieldname": "column_break_tax_info",
				"fieldtype": "Column Break",
				"insert_after": "customer_vrn",
			},
			{
				"fieldname": "company_tin",
				"fieldtype": "Data",
				"label": _("Company TIN"),
				"fetch_from": "company.tin",
				"read_only": 1,
				"insert_after": "column_break_tax_info",
			},
			{
				"fieldname": "company_vrn",
				"fieldtype": "Data",
				"label": _("Company VRN"),
				"fetch_from": "company.vrn",
				"read_only": 1,
				"insert_after": "company_tin",
			},
		],
		"Purchase Invoice": [
			{
				"fieldname": "tanzania_tax_section",
				"fieldtype": "Section Break",
				"label": _("Tanzania Tax Information"),
				"insert_after": "taxes_section",
			},
			{
				"fieldname": "supplier_tin",
				"fieldtype": "Data",
				"label": _("Supplier TIN"),
				"fetch_from": "supplier.tin",
				"read_only": 1,
				"insert_after": "tanzania_tax_section",
			},
			{
				"fieldname": "supplier_vrn",
				"fieldtype": "Data",
				"label": _("Supplier VRN"),
				"fetch_from": "supplier.vrn",
				"read_only": 1,
				"insert_after": "supplier_tin",
			},
			{
				"fieldname": "column_break_tax_info",
				"fieldtype": "Column Break",
				"insert_after": "supplier_vrn",
			},
			{
				"fieldname": "company_tin",
				"fieldtype": "Data",
				"label": _("Company TIN"),
				"fetch_from": "company.tin",
				"read_only": 1,
				"insert_after": "column_break_tax_info",
			},
			{
				"fieldname": "company_vrn",
				"fieldtype": "Data",
				"label": _("Company VRN"),
				"fetch_from": "company.vrn",
				"read_only": 1,
				"insert_after": "company_tin",
			},
		],
	}


def create_tanzania_custom_fields():
	"""Create custom fields for Tanzania tax and payroll compliance"""
	custom_fields = get_tanzania_custom_fields()
	create_custom_fields(custom_fields, ignore_validate=True)
	frappe.msgprint(_("Tanzania tax and payroll compliance custom fields created successfully"))
