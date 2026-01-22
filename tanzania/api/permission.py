# Copyright (c) 2024, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe


def has_app_permission():
	"""Check if user has permission to access the Tanzania app"""
	if frappe.session.user == "Administrator":
		return True

	# Check if user has access to relevant doctypes
	if frappe.has_permission("Sales Invoice", ptype="read"):
		return True

	if frappe.has_permission("Employee", ptype="read"):
		return True

	if frappe.has_permission("Company", ptype="read"):
		return True

	return False
