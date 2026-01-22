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
			# Statutory Details Section - Clean 4-column grid layout
			{
				"fieldname": "statutory_details_section",
				"fieldtype": "Section Break",
				"label": _("Statutory Details"),
				"insert_after": "salary_mode",
			},
			# Row 1 - Column 1
			{
				"fieldname": "pension_fund",
				"fieldtype": "Select",
				"label": _("Pension Fund"),
				"options": "\nNSSF\nPSSF",
				"insert_after": "statutory_details_section",
			},
			{
				"fieldname": "col_break_stat_1",
				"fieldtype": "Column Break",
				"insert_after": "pension_fund",
			},
			# Row 1 - Column 2
			{
				"fieldname": "employee_tin",
				"fieldtype": "Data",
				"label": _("TIN"),
				"insert_after": "col_break_stat_1",
			},
			{
				"fieldname": "col_break_stat_2",
				"fieldtype": "Column Break",
				"insert_after": "employee_tin",
			},
			# Row 1 - Column 3
			{
				"fieldname": "heslb",
				"fieldtype": "Data",
				"label": _("HESLB"),
				"insert_after": "col_break_stat_2",
			},
			# Row 2
			{
				"fieldname": "section_break_stat_row2",
				"fieldtype": "Section Break",
				"insert_after": "heslb",
			},
			# Row 2 - Column 1
			{
				"fieldname": "pension_fund_number",
				"fieldtype": "Data",
				"label": _("Pension Fund Number"),
				"insert_after": "section_break_stat_row2",
			},
			{
				"fieldname": "col_break_stat_4",
				"fieldtype": "Column Break",
				"insert_after": "pension_fund_number",
			},
			# Row 2 - Column 2
			{
				"fieldname": "wcf_number",
				"fieldtype": "Data",
				"label": _("WCF Number"),
				"insert_after": "col_break_stat_4",
			},
			{
				"fieldname": "col_break_stat_5",
				"fieldtype": "Column Break",
				"insert_after": "wcf_number",
			},
			# Row 2 - Column 3
			{
				"fieldname": "national_identity",
				"fieldtype": "Data",
				"label": _("National Identity"),
				"insert_after": "col_break_stat_5",
			},
			{
				"fieldname": "col_break_stat_6",
				"fieldtype": "Column Break",
				"insert_after": "national_identity",
			},
			# Row 2 - Column 4
			{
				"fieldname": "nida",
				"fieldtype": "Data",
				"label": _("NIDA"),
				"insert_after": "col_break_stat_6",
			},
			# Employment Type (separate section or can be added to existing)
			{
				"fieldname": "employment_type_section",
				"fieldtype": "Section Break",
				"insert_after": "nida",
			},
			{
				"fieldname": "employment_type",
				"fieldtype": "Select",
				"label": _("Employment Type"),
				"options": "Primary\nSecondary",
				"description": _("Primary or Secondary employment (affects PAYE calculation)"),
				"insert_after": "employment_type_section",
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
				"fieldname": "efd_id_type",
				"fieldtype": "Select",
				"label": _("EFD ID Type"),
				"options": "\n1-TIN\n2-Driving License\n3-Voter ID\n4-Passport\n5-NID\n6-Other",
				"description": _("Customer identification type for EFD receipts"),
				"insert_after": "column_break_tax_info",
			},
			{
				"fieldname": "tax_category",
				"fieldtype": "Link",
				"label": _("Tax Category"),
				"options": "Tax Category",
				"insert_after": "efd_id_type",
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
			# EFD Fields
			{
				"fieldname": "efd_section",
				"fieldtype": "Section Break",
				"label": _("EFD Information"),
				"insert_after": "company_vrn",
				"collapsible": 1,
			},
			{
				"fieldname": "efd_status",
				"fieldtype": "Select",
				"label": _("EFD Status"),
				"options": "Not Sent\nPending\nSuccess\nFailed",
				"default": "Not Sent",
				"read_only": 1,
				"allow_on_submit": 1,
				"insert_after": "efd_section",
				"in_list_view": 1,
			},
			{
				"fieldname": "efd_receipt_number",
				"fieldtype": "Data",
				"label": _("Receipt Number"),
				"read_only": 1,
				"allow_on_submit": 1,
				"insert_after": "efd_status",
			},
			{
				"fieldname": "column_break_efd",
				"fieldtype": "Column Break",
				"insert_after": "efd_receipt_number",
			},
			{
				"fieldname": "efd_verification_url",
				"fieldtype": "Data",
				"label": _("Verification URL"),
				"read_only": 1,
				"allow_on_submit": 1,
				"insert_after": "column_break_efd",
			},
			{
				"fieldname": "efd_posting_log",
				"fieldtype": "Link",
				"label": _("EFD Posting Log"),
				"options": "EFD Posting Log",
				"read_only": 1,
				"allow_on_submit": 1,
				"insert_after": "efd_verification_url",
			},
			{
				"fieldname": "efd_settings_section",
				"fieldtype": "Section Break",
				"label": _("EFD Settings"),
				"insert_after": "efd_posting_log",
				"collapsible": 1,
			},
			{
				"fieldname": "skip_efd",
				"fieldtype": "Check",
				"label": _("Skip EFD"),
				"description": _("Check to exclude this invoice from EFD submission"),
				"insert_after": "efd_settings_section",
			},
			{
				"fieldname": "auto_submit_efd",
				"fieldtype": "Check",
				"label": _("Auto Submit EFD"),
				"description": _("Automatically submit to TRA on invoice submit"),
				"default": "1",
				"insert_after": "skip_efd",
			},
			{
				"fieldname": "column_break_efd_settings",
				"fieldtype": "Column Break",
				"insert_after": "auto_submit_efd",
			},
			{
				"fieldname": "efd_date",
				"fieldtype": "Date",
				"label": _("EFD Date"),
				"read_only": 1,
				"allow_on_submit": 1,
				"insert_after": "column_break_efd_settings",
			},
			{
				"fieldname": "efd_time",
				"fieldtype": "Time",
				"label": _("EFD Time"),
				"read_only": 1,
				"allow_on_submit": 1,
				"insert_after": "efd_date",
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
		"Item Tax Template": [
			{
				"fieldname": "efd_tax_code",
				"fieldtype": "Select",
				"label": _("EFD Tax Code"),
				"options": "\nA-Standard 18%\nB-Special Rate\nC-Zero Rated\nD-Special Relief\nE-Exempt",
				"description": _("Tax rate code for EFD receipts (A=18%, B=Special, C=Zero, D=Relief, E=Exempt)"),
				"insert_after": "title",
			},
		],
		"Mode of Payment": [
			{
				"fieldname": "efd_payment_type",
				"fieldtype": "Select",
				"label": _("EFD Payment Type"),
				"options": "\nCASH\nCHEQUE\nCCARD\nEMONEY\nINVOICE",
				"description": _("Payment type for EFD receipts"),
				"insert_after": "type",
			},
		],
	}


def create_tanzania_custom_fields():
	"""Create custom fields for Tanzania tax and payroll compliance"""
	custom_fields = get_tanzania_custom_fields()
	create_custom_fields(custom_fields, ignore_validate=True)
	frappe.msgprint(_("Tanzania tax and payroll compliance custom fields created successfully"))
