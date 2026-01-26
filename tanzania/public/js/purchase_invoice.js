/**
 * Tanzania Tax Integration for Purchase Invoice
 * Auto-populates Item Tax Template
 */

// Auto-populate Item Tax Template when item is selected
frappe.ui.form.on('Purchase Invoice Item', {
	item_code: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.item_code && frm.doc.company) {
			// Fetch Item Tax Template from Item's taxes child table
			frappe.call({
				method: 'frappe.client.get',
				args: {
					doctype: 'Item',
					name: row.item_code
				},
				callback: function(r) {
					if (r.message && r.message.taxes && r.message.taxes.length > 0) {
						// Find tax template for the company or first one
						let tax_row = r.message.taxes.find(t => !t.tax_category) || r.message.taxes[0];
						if (tax_row && tax_row.item_tax_template) {
							frappe.model.set_value(cdt, cdn, 'item_tax_template', tax_row.item_tax_template);
						}
					} else if (r.message && r.message.item_group) {
						// Try to get from Item Group
						frappe.call({
							method: 'frappe.client.get',
							args: {
								doctype: 'Item Group',
								name: r.message.item_group
							},
							callback: function(gr) {
								if (gr.message && gr.message.taxes && gr.message.taxes.length > 0) {
									let tax_row = gr.message.taxes.find(t => !t.tax_category) || gr.message.taxes[0];
									if (tax_row && tax_row.item_tax_template) {
										frappe.model.set_value(cdt, cdn, 'item_tax_template', tax_row.item_tax_template);
									}
								}
							}
						});
					}
				}
			});
		}
	}
});
