// Copyright (c) 2024, Navari Limited and contributors
// For license information, please see license.txt

frappe.query_reports["PAYE and SDL Report"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department"
		}
	],

	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		// Highlight PAYE column in green
		if (column.fieldname == "paye" && data && data.paye > 0) {
			value = "<span style='color:green; font-weight:bold'>" + value + "</span>";
		}

		// Highlight SDL column in green
		if (column.fieldname == "sdl" && data && data.sdl > 0) {
			value = "<span style='color:green; font-weight:bold'>" + value + "</span>";
		}

		return value;
	},

	onload: function(report) {
		// Add custom buttons for export
		report.page.add_inner_button(__("Export for TRA"), function() {
			frappe.msgprint(__("Exporting report for TRA submission..."));
			// TODO: Add custom export logic for TRA format
		});
	}
};
