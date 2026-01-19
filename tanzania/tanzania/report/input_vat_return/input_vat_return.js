// Copyright (c) 2024, Navari Limited and contributors
// For license information, please see license.txt

frappe.query_reports["Input VAT Return"] = {
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
			"fieldname": "supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier"
		}
	],

	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname == "vat_amount" && data && data.vat_amount > 0) {
			value = "<span style='color:green; font-weight:bold'>" + value + "</span>";
		}

		// Highlight missing TIN/VRN
		if ((column.fieldname == "supplier_tin" || column.fieldname == "supplier_vrn") && data) {
			if (!data[column.fieldname]) {
				value = "<span style='color:orange'>Missing</span>";
			}
		}

		return value;
	},

	onload: function(report) {
		report.page.add_inner_button(__("Input VAT Summary"), function() {
			frappe.call({
				method: "tanzania.tanzania.report.input_vat_return.input_vat_return.get_input_vat_summary",
				args: {
					filters: report.get_values()
				},
				callback: function(r) {
					if (r.message) {
						frappe.msgprint({
							title: __("Input VAT Summary"),
							message: `
								<table class="table table-bordered">
									<tr>
										<td><strong>Total Invoices:</strong></td>
										<td>${r.message.invoice_count}</td>
									</tr>
									<tr>
										<td><strong>Total Taxable Amount:</strong></td>
										<td>${format_currency(r.message.total_taxable)}</td>
									</tr>
									<tr>
										<td><strong>Total Input VAT:</strong></td>
										<td><strong style="color:green">${format_currency(r.message.total_vat)}</strong></td>
									</tr>
									<tr>
										<td><strong>Total Amount:</strong></td>
										<td>${format_currency(r.message.total_amount)}</td>
									</tr>
								</table>
								<p class="text-muted">Input VAT can be claimed against Output VAT in your VAT Return</p>
							`,
							indicator: 'green'
						});
					}
				}
			});
		});

		report.page.add_inner_button(__("Export for TRA"), function() {
			frappe.msgprint(__("Exporting Input VAT data for TRA eFiling..."));
			// TODO: Add TRA-specific export format
		});
	}
};
