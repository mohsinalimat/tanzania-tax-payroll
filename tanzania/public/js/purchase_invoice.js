/**
 * Tanzania Tax Integration for Purchase Invoice
 * Auto-populates Item Tax Template and sets matching Taxes and Charges Template
 */

// Auto-populate Item Tax Template and set matching Taxes and Charges Template
frappe.ui.form.on('Purchase Invoice Item', {
	item_code: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.item_code && frm.doc.company) {
			tanzania_tax.set_item_tax_template(frm, cdt, cdn, row.item_code, 'Purchase');
		}
	}
});
