// Copyright (c) 2024, Navari Limited and contributors
// For license information, please see license.txt

frappe.query_reports["Monthly Payroll Summary"] = {
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
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department"
		}
	],

	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		// Highlight total cost column
		if (column.fieldname == "total_cost" && data && data.total_cost > 0) {
			value = "<span style='color:red; font-weight:bold'>" + value + "</span>";
		}

		// Highlight net pay column
		if (column.fieldname == "net_pay" && data && data.net_pay > 0) {
			value = "<span style='color:green; font-weight:bold'>" + value + "</span>";
		}

		return value;
	},

	onload: function(report) {
		// Add custom button for executive summary
		report.page.add_inner_button(__("Executive Summary"), function() {
			let data = report.data;
			if (data && data.length > 0) {
				let total_employees = 0;
				let total_gross = 0;
				let total_net = 0;
				let total_cost = 0;
				let total_paye = 0;
				let total_nssf_employee = 0;
				let total_nssf_employer = 0;
				let total_sdl = 0;
				let total_wcf = 0;

				data.forEach(row => {
					total_employees += row.employee_count || 0;
					total_gross += row.gross_pay || 0;
					total_net += row.net_pay || 0;
					total_cost += row.total_cost || 0;
					total_paye += row.paye || 0;
					total_nssf_employee += row.nssf_employee || 0;
					total_nssf_employer += row.nssf_employer || 0;
					total_sdl += row.sdl || 0;
					total_wcf += row.wcf || 0;
				});

				let avg_gross = total_employees > 0 ? total_gross / total_employees : 0;
				let avg_net = total_employees > 0 ? total_net / total_employees : 0;

				frappe.msgprint({
					title: __("Executive Payroll Summary"),
					message: `
						<div style="font-size: 14px;">
							<h4 style="border-bottom: 2px solid #2c5282; padding-bottom: 10px;">
								Workforce & Costs
							</h4>
							<table class="table table-bordered" style="margin-bottom: 20px;">
								<tr>
									<td><strong>Total Employees:</strong></td>
									<td style="text-align: right;">${total_employees}</td>
								</tr>
								<tr>
									<td><strong>Total Gross Pay:</strong></td>
									<td style="text-align: right;">${format_currency(total_gross)}</td>
								</tr>
								<tr>
									<td><strong>Total Net Pay:</strong></td>
									<td style="text-align: right;">${format_currency(total_net)}</td>
								</tr>
								<tr style="background-color: #fff3cd;">
									<td><strong>Total Cost to Company:</strong></td>
									<td style="text-align: right;"><strong>${format_currency(total_cost)}</strong></td>
								</tr>
							</table>

							<h4 style="border-bottom: 2px solid #2c5282; padding-bottom: 10px;">
								Average Per Employee
							</h4>
							<table class="table table-bordered" style="margin-bottom: 20px;">
								<tr>
									<td><strong>Average Gross Pay:</strong></td>
									<td style="text-align: right;">${format_currency(avg_gross)}</td>
								</tr>
								<tr>
									<td><strong>Average Net Pay:</strong></td>
									<td style="text-align: right;">${format_currency(avg_net)}</td>
								</tr>
							</table>

							<h4 style="border-bottom: 2px solid #2c5282; padding-bottom: 10px;">
								Statutory Obligations
							</h4>
							<table class="table table-bordered">
								<tr>
									<td><strong>PAYE (Employee Tax):</strong></td>
									<td style="text-align: right;">${format_currency(total_paye)}</td>
								</tr>
								<tr>
									<td><strong>NSSF Employee (10%):</strong></td>
									<td style="text-align: right;">${format_currency(total_nssf_employee)}</td>
								</tr>
								<tr>
									<td><strong>NSSF Employer (10%):</strong></td>
									<td style="text-align: right;">${format_currency(total_nssf_employer)}</td>
								</tr>
								<tr>
									<td><strong>SDL (3.5%):</strong></td>
									<td style="text-align: right;">${format_currency(total_sdl)}</td>
								</tr>
								<tr>
									<td><strong>WCF (0.5%):</strong></td>
									<td style="text-align: right;">${format_currency(total_wcf)}</td>
								</tr>
								<tr style="background-color: #f8d7da;">
									<td><strong>Total Statutory:</strong></td>
									<td style="text-align: right;"><strong>${format_currency(
										total_paye + total_nssf_employee + total_nssf_employer + total_sdl + total_wcf
									)}</strong></td>
								</tr>
							</table>
						</div>
					`,
					indicator: 'blue',
					wide: true
				});
			}
		});

		// Add button to export for management
		report.page.add_inner_button(__("Export for Management"), function() {
			frappe.msgprint(__("Generating management report..."));
			// TODO: Add custom export logic for management presentation
		});
	}
};
