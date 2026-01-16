// Copyright (c) 2024, Navari Limited and contributors
// For license information, please see license.txt

frappe.query_reports["NSSF Contribution Report"] = {
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
			"options": "Employee",
			"get_query": function() {
				return {
					"filters": {
						"nssf": 1
					}
				};
			}
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

		// Highlight total contribution column
		if (column.fieldname == "total_contribution" && data && data.total_contribution > 0) {
			value = "<span style='color:green; font-weight:bold'>" + value + "</span>";
		}

		// Highlight running total
		if (column.fieldname == "running_total" && data && data.running_total > 0) {
			value = "<span style='color:blue; font-weight:bold'>" + value + "</span>";
		}

		return value;
	},

	onload: function(report) {
		// Add custom button for NSSF export
		report.page.add_inner_button(__("Export for NSSF"), function() {
			frappe.msgprint(__("Exporting report in NSSF Form CON.5 format..."));
			// TODO: Add custom export logic for NSSF submission
		});

		// Add button to show summary
		report.page.add_inner_button(__("Show Summary"), function() {
			let data = report.data;
			if (data && data.length > 0) {
				let total_employee = 0;
				let total_employer = 0;
				let total_contribution = 0;

				data.forEach(row => {
					total_employee += row.employee_contribution || 0;
					total_employer += row.employer_contribution || 0;
					total_contribution += row.total_contribution || 0;
				});

				frappe.msgprint({
					title: __("NSSF Contribution Summary"),
					message: `
						<table class="table table-bordered">
							<tr>
								<td><strong>Total Employees:</strong></td>
								<td>${data.length}</td>
							</tr>
							<tr>
								<td><strong>Employee Contributions:</strong></td>
								<td>${format_currency(total_employee)}</td>
							</tr>
							<tr>
								<td><strong>Employer Contributions:</strong></td>
								<td>${format_currency(total_employer)}</td>
							</tr>
							<tr>
								<td><strong>Total Contributions:</strong></td>
								<td><strong>${format_currency(total_contribution)}</strong></td>
							</tr>
						</table>
					`,
					indicator: 'green'
				});
			}
		});
	}
};
