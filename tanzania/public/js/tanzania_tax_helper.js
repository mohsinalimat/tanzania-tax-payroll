/**
 * Tanzania Tax Helper Module
 * Shared utilities for tax template management
 */

const tanzania_tax = {
	/**
	 * Set Item Tax Template and matching document taxes
	 */
	set_item_tax_template: function(frm, cdt, cdn, item_code, doc_type) {
		frappe.call({
			method: 'frappe.client.get',
			args: {
				doctype: 'Item',
				name: item_code
			},
			callback: function(r) {
				let item_tax_template = null;

				if (r.message && r.message.taxes && r.message.taxes.length > 0) {
					let tax_row = r.message.taxes.find(t => !t.tax_category) || r.message.taxes[0];
					if (tax_row && tax_row.item_tax_template) {
						item_tax_template = tax_row.item_tax_template;
						frappe.model.set_value(cdt, cdn, 'item_tax_template', item_tax_template);
					}
				}

				// If no item tax template, try Item Group
				if (!item_tax_template && r.message && r.message.item_group) {
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
									item_tax_template = tax_row.item_tax_template;
									frappe.model.set_value(cdt, cdn, 'item_tax_template', item_tax_template);
								}
							}
							// Set document taxes after getting from Item Group
							tanzania_tax.set_document_taxes(frm, item_tax_template, doc_type);
						}
					});
				} else {
					// Set document taxes with item's template
					tanzania_tax.set_document_taxes(frm, item_tax_template, doc_type);
				}
			}
		});
	},

	/**
	 * Set document-level taxes based on Item Tax Template
	 */
	set_document_taxes: function(frm, item_tax_template, doc_type) {
		if (!item_tax_template) return;

		// Determine the tax type from Item Tax Template name
		let is_zero_or_exempt = item_tax_template.toLowerCase().includes('zero') ||
							   item_tax_template.toLowerCase().includes('exempt');

		// Get the appropriate taxes template suffix
		let template_suffix = is_zero_or_exempt ? 'Zero Rated' : 'VAT 18%';

		// Find matching template for the company
		frappe.call({
			method: 'frappe.client.get_list',
			args: {
				doctype: doc_type === 'Sales' ? 'Sales Taxes and Charges Template' : 'Purchase Taxes and Charges Template',
				filters: {
					company: frm.doc.company,
					title: ['like', `%${template_suffix}%`]
				},
				fields: ['name'],
				limit_page_length: 1
			},
			async: false,
			callback: function(r) {
				if (r.message && r.message.length > 0) {
					let new_template = r.message[0].name;
					let current_template = frm.doc.taxes_and_charges || '';

					// Only change if current template doesn't match the item's tax type
					let current_is_zero = current_template.toLowerCase().includes('zero');
					let need_zero = is_zero_or_exempt;

					if (current_is_zero !== need_zero) {
						frm.set_value('taxes_and_charges', new_template);
						// Trigger tax calculation
						frm.trigger('taxes_and_charges');
					}
				}
			}
		});
	}
};
