// Copyright (c) 2024, Navari Limited and contributors
// For license information, please see license.txt

frappe.query_reports["HESLB Return"] = {
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
			"default": frappe.datetime.month_start(),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_end(),
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
						"heslb": 1
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

		if (column.fieldname == "heslb_deduction" && data && data.heslb_deduction > 0) {
			value = "<span style='color:blue; font-weight:bold'>" + value + "</span>";
		}

		// Highlight missing NIDA
		if (column.fieldname == "nida_no" && data && !data.nida_no) {
			value = "<span style='color:orange'>Missing NIDA</span>";
		}

		return value;
	},

	onload: function(report) {
		report.page.add_inner_button(__("HESLB Summary"), function() {
			frappe.call({
				method: "tanzania.tanzania.report.heslb_return.heslb_return.get_heslb_summary",
				args: {
					filters: report.get_values()
				},
				callback: function(r) {
					if (r.message) {
						frappe.msgprint({
							title: __("HESLB Deduction Summary"),
							message: `
								<table class="table table-bordered">
									<tr>
										<td><strong>Total Employees with HESLB:</strong></td>
										<td>${r.message.total_employees}</td>
									</tr>
									<tr>
										<td><strong>Total Gross Salary:</strong></td>
										<td>${format_currency(r.message.total_gross_salary)}</td>
									</tr>
									<tr>
										<td><strong>Total HESLB Deduction:</strong></td>
										<td><strong style="color:blue">${format_currency(r.message.total_heslb_deduction)}</strong></td>
									</tr>
									<tr>
										<td><strong>Average Deduction per Employee:</strong></td>
										<td>${format_currency(r.message.average_deduction)}</td>
									</tr>
								</table>
								<p class="text-muted">HESLB remittance due by 30th of following month</p>
							`,
							indicator: 'blue'
						});
					}
				}
			});
		});

		report.page.add_inner_button(__("Export for HESLB Portal"), function() {
			frappe.call({
				method: "tanzania.tanzania.report.heslb_return.heslb_return.export_heslb_excel",
				args: {
					filters: report.get_values()
				},
				callback: function(r) {
					if (r.message) {
						frappe.msgprint({
							title: __("HESLB Export"),
							message: __("Data ready for HESLB portal upload. {0} records prepared.", [r.message.length]),
							indicator: 'green'
						});
						// TODO: Trigger actual Excel download
					}
				}
			});
		});
	}
};
