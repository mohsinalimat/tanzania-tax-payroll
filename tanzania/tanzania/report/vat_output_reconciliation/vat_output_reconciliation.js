// Copyright (c) 2024, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.query_reports["VAT Output Reconciliation"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			reqd: 1
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1
		},
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer"
		},
		{
			fieldname: "efd_status",
			label: __("EFD Status"),
			fieldtype: "Select",
			options: "\nNot Sent\nPending\nSuccess\nFailed"
		},
		{
			fieldname: "vat_only",
			label: __("VAT Invoices Only"),
			fieldtype: "Check",
			default: 1
		},
		{
			fieldname: "include_efd",
			label: __("Include EFD Details"),
			fieldtype: "Check",
			default: 1
		}
	],

	formatter: function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "efd_status") {
			if (data.efd_status === "Success") {
				value = `<span class="indicator-pill green">${value}</span>`;
			} else if (data.efd_status === "Failed") {
				value = `<span class="indicator-pill red">${value}</span>`;
			} else if (data.efd_status === "Pending") {
				value = `<span class="indicator-pill orange">${value}</span>`;
			} else if (data.efd_status === "Not Sent" || !data.efd_status) {
				value = `<span class="indicator-pill grey">Not Sent</span>`;
			}
		}

		if (column.fieldname === "vat_amount" && data.vat_amount > 0) {
			value = `<span style="font-weight: bold;">${value}</span>`;
		}

		return value;
	}
};
