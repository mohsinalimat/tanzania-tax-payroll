// Copyright (c) 2024, Navari Limited and contributors
// For license information, please see license.txt

frappe.query_reports["VAT eFiling Return"] = {
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
		}
	],

	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (data) {
			// Bold section headers
			if (data.section && ["A", "B", "C"].includes(data.section)) {
				value = "<b>" + value + "</b>";
			}
			// Highlight totals
			if (data.section && ["A4", "B4", "C3"].includes(data.section)) {
				if (column.fieldname == "vat_amount") {
					let color = data.section == "C3" ?
						(data.vat_amount >= 0 ? "red" : "green") : "blue";
					value = "<span style='color:" + color + "; font-weight:bold'>" + value + "</span>";
				}
			}
		}

		return value;
	},

	onload: function(report) {
		report.page.add_inner_button(__("VAT Summary"), function() {
			frappe.call({
				method: "tanzania.tanzania.report.vat_efiling_return.vat_efiling_return.get_vat_summary",
				args: {
					filters: report.get_values()
				},
				callback: function(r) {
					if (r.message) {
						let status_color = r.message.status == "PAYABLE" ? "red" : "green";
						frappe.msgprint({
							title: __("VAT eFiling Summary"),
							message: `
								<table class="table table-bordered">
									<tr>
										<td><strong>Total Output VAT (Sales):</strong></td>
										<td>${format_currency(r.message.total_output_vat)}</td>
									</tr>
									<tr>
										<td><strong>Total Input VAT (Purchases):</strong></td>
										<td>${format_currency(r.message.total_input_vat)}</td>
									</tr>
									<tr style="background-color: #f5f5f5">
										<td><strong>Net VAT:</strong></td>
										<td><strong style="color: ${status_color}">${format_currency(Math.abs(r.message.net_vat))} (${r.message.status})</strong></td>
									</tr>
								</table>
								<p class="text-muted">VAT Return due by 20th of following month</p>
							`,
							indicator: r.message.status == "PAYABLE" ? 'red' : 'green'
						});
					}
				}
			});
		});

		report.page.add_inner_button(__("Export for TRA"), function() {
			frappe.msgprint(__("Exporting VAT Return for TRA eFiling submission..."));
			// TODO: Add TRA eFiling export format
		});
	}
};
