// Copyright (c) 2024, Navari Limited and contributors
// For license information, please see license.txt

frappe.query_reports["ITX 219 03 E Withholding Tax"] = {
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
			"default": frappe.datetime.add_months(frappe.datetime.month_start(), 0),
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
			"fieldname": "supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier"
		}
	],

	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname == "wht_amount" && data && data.wht_amount > 0) {
			value = "<span style='color:green; font-weight:bold'>" + value + "</span>";
		}

		return value;
	},

	onload: function(report) {
		report.page.add_inner_button(__("Show Summary"), function() {
			frappe.call({
				method: "tanzania.tanzania.report.itx_219_03_e_withholding_tax.itx_219_03_e_withholding_tax.get_wht_summary",
				args: {
					filters: report.get_values()
				},
				callback: function(r) {
					if (r.message) {
						frappe.msgprint({
							title: __("ITX.219.03.E Summary"),
							message: `
								<table class="table table-bordered">
									<tr>
										<td><strong>Total Transactions:</strong></td>
										<td>${r.message.total_transactions}</td>
									</tr>
									<tr>
										<td><strong>Total Gross Amount:</strong></td>
										<td>${format_currency(r.message.total_gross_amount)}</td>
									</tr>
									<tr>
										<td><strong>Total WHT Amount:</strong></td>
										<td><strong>${format_currency(r.message.total_wht_amount)}</strong></td>
									</tr>
								</table>
								<p class="text-muted">Submit this amount to TRA by 7th of following month</p>
							`,
							indicator: 'blue'
						});
					}
				}
			});
		});

		report.page.add_inner_button(__("Export for TRA"), function() {
			frappe.msgprint(__("Exporting report in ITX.219.03.E format for TRA submission..."));
			// TODO: Add TRA-specific export format
		});
	}
};
