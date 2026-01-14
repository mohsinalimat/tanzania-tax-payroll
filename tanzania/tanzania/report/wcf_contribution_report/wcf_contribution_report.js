// Copyright (c) 2024, Navari Limited and contributors
// For license information, please see license.txt

frappe.query_reports["WCF Contribution Report"] = {
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

		// Highlight WCF contribution column
		if (column.fieldname == "wcf_contribution" && data && data.wcf_contribution > 0) {
			value = "<span style='color:green; font-weight:bold'>" + value + "</span>";
		}

		// Highlight running total
		if (column.fieldname == "running_total" && data && data.running_total > 0) {
			value = "<span style='color:blue; font-weight:bold'>" + value + "</span>";
		}

		return value;
	},

	onload: function(report) {
		// Add custom button for WCF export
		report.page.add_inner_button(__("Export for WCF"), function() {
			frappe.msgprint(__("Exporting report for WCF submission..."));
			// TODO: Add custom export logic for WCF submission
		});

		// Add button to show summary
		report.page.add_inner_button(__("Show Summary"), function() {
			let data = report.data;
			if (data && data.length > 0) {
				let total_wcf = 0;

				data.forEach(row => {
					total_wcf += row.wcf_contribution || 0;
				});

				frappe.msgprint({
					title: __("WCF Contribution Summary"),
					message: `
						<table class="table table-bordered">
							<tr>
								<td><strong>Total Employees:</strong></td>
								<td>${data.length}</td>
							</tr>
							<tr>
								<td><strong>Total WCF Contribution (0.5%):</strong></td>
								<td><strong>${format_currency(total_wcf)}</strong></td>
							</tr>
							<tr>
								<td colspan="2">
									<em>Note: WCF is employer-only contribution (0.5% of gross pay)</em>
								</td>
							</tr>
						</table>
					`,
					indicator: 'green'
				});
			}
		});
	}
};
