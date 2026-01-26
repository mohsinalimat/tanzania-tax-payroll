/**
 * Tanzania EFD Integration for Sales Invoice
 * Adds EFD submission button and preview dialog
 */

frappe.ui.form.on('Sales Invoice', {
	refresh: function(frm) {
		// Add EFD button for submitted invoices
		if (frm.doc.docstatus === 1 && !frm.doc.is_return && !frm.doc.skip_efd) {
			if (frm.doc.efd_status !== 'Success') {
				frm.add_custom_button(__('Submit to EFD'), function() {
					tanzania_efd.show_preview(frm);
				}, __('EFD'));
			}

			if (frm.doc.efd_status === 'Success' && frm.doc.efd_verification_url) {
				frm.add_custom_button(__('Verify Receipt'), function() {
					window.open(frm.doc.efd_verification_url, '_blank');
				}, __('EFD'));
			}
		}

		// Show EFD status indicator
		tanzania_efd.show_status_indicator(frm);
	}
});

// Auto-populate Item Tax Template and set matching Taxes and Charges Template
frappe.ui.form.on('Sales Invoice Item', {
	item_code: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.item_code && frm.doc.company) {
			tanzania_tax.set_item_tax_template(frm, cdt, cdn, row.item_code, 'Sales');
		}
	}
});


/**
 * Tanzania EFD Module
 */
const tanzania_efd = {
	/**
	 * Show EFD preview dialog
	 */
	show_preview: function(frm) {
		frappe.call({
			method: 'tanzania.efd.utils.submit_efd_receipt',
			args: {
				invoice_name: frm.doc.name,
				preview: true
			},
			freeze: true,
			freeze_message: __('Loading EFD Preview...'),
			callback: function(r) {
				if (r.message && r.message.success) {
					tanzania_efd.render_preview_dialog(frm, r.message);
				} else {
					frappe.msgprint({
						title: __('EFD Error'),
						message: r.message ? r.message.message : __('Failed to load preview'),
						indicator: 'red'
					});
				}
			}
		});
	},

	/**
	 * Render preview dialog with payload data
	 */
	render_preview_dialog: function(frm, data) {
		const payload = data.payload;
		const provider = data.provider;

		// Normalize payload across providers
		const normalized = tanzania_efd.normalize_payload(payload, provider);

		// Build HTML content
		let html = `
			<div class="efd-preview">
				<h5>${__('Provider')}: ${provider}</h5>
				<hr>

				<h6>${__('Customer Information')}</h6>
				<table class="table table-bordered table-sm">
					<tr><td><strong>${__('Name')}</strong></td><td>${normalized.customer.name || '-'}</td></tr>
					<tr><td><strong>${__('ID Type')}</strong></td><td>${normalized.customer.id_type || '-'}</td></tr>
					<tr><td><strong>${__('ID Value')}</strong></td><td>${normalized.customer.id_value || '-'}</td></tr>
				</table>

				<h6>${__('Items')}</h6>
				<table class="table table-bordered table-sm">
					<thead>
						<tr>
							<th>${__('Item')}</th>
							<th class="text-right">${__('Qty')}</th>
							<th class="text-right">${__('Price')}</th>
							<th>${__('Tax')}</th>
							<th class="text-right">${__('Amount')}</th>
						</tr>
					</thead>
					<tbody>
						${normalized.items.map(item => `
							<tr>
								<td>${item.name}</td>
								<td class="text-right">${item.qty}</td>
								<td class="text-right">${format_currency(item.unit_price)}</td>
								<td>${item.tax_code}</td>
								<td class="text-right">${format_currency(item.amount)}</td>
							</tr>
						`).join('')}
					</tbody>
					<tfoot>
						<tr>
							<td colspan="4" class="text-right"><strong>${__('Total')}</strong></td>
							<td class="text-right"><strong>${format_currency(normalized.total)}</strong></td>
						</tr>
					</tfoot>
				</table>

				<h6>${__('Payment')}</h6>
				<table class="table table-bordered table-sm">
					<tr><td><strong>${__('Type')}</strong></td><td>${normalized.payment.type}</td></tr>
					<tr><td><strong>${__('Amount')}</strong></td><td>${format_currency(normalized.payment.amount)}</td></tr>
				</table>
			</div>
		`;

		// Show dialog
		let d = new frappe.ui.Dialog({
			title: __('EFD Receipt Preview'),
			size: 'large',
			fields: [
				{
					fieldtype: 'HTML',
					fieldname: 'preview_html',
					options: html
				}
			],
			primary_action_label: __('Submit to TRA'),
			primary_action: function() {
				d.hide();
				tanzania_efd.submit_receipt(frm);
			},
			secondary_action_label: __('Cancel')
		});

		d.show();
	},

	/**
	 * Normalize payload across different providers
	 */
	normalize_payload: function(payload, provider) {
		let normalized = {
			customer: { name: '', id_type: '', id_value: '' },
			items: [],
			payment: { type: 'INVOICE', amount: 0 },
			total: 0
		};

		try {
			if (provider === 'VFDPlus') {
				// VFDPlus format
				const cust = payload.customer_info || {};
				normalized.customer = {
					name: cust.cust_name || '',
					id_type: tanzania_efd.id_type_label(cust.cust_id_type),
					id_value: cust.cust_id || ''
				};

				normalized.items = (payload.cart_items || []).map(item => ({
					name: item.item_name || '',
					qty: item.item_qty || 0,
					unit_price: item.usp || 0,
					tax_code: `${item.vat_rate_code || 'A'} (${tanzania_efd.tax_code_label(item.vat_rate_code)})`,
					amount: item.sp || 0
				}));

				const pmt = (payload.payment_methods || [])[0] || {};
				normalized.payment = {
					type: pmt.pmt_type || 'INVOICE',
					amount: pmt.pmt_amount || 0
				};

				normalized.total = (payload.cart_totals || {}).total_amount || 0;

			} else if (provider === 'TotalVFD') {
				// TotalVFD format
				const cust = payload.customer || {};
				normalized.customer = {
					name: cust.name || '',
					id_type: tanzania_efd.id_type_label(cust.idType),
					id_value: cust.idValue || ''
				};

				normalized.items = (payload.items || []).map(item => ({
					name: item.name || item.id || '',
					qty: item.qty || 0,
					unit_price: item.price || 0,
					tax_code: `${item.vatGroup || 'A'} (${tanzania_efd.tax_code_label(item.vatGroup)})`,
					amount: (item.price || 0) * (item.qty || 0)
				}));

				const pmt = (payload.payments || [])[0] || {};
				normalized.payment = {
					type: (pmt.type || 'invoice').toUpperCase(),
					amount: pmt.amount || 0
				};

				normalized.total = normalized.items.reduce((sum, item) => sum + item.amount, 0);

			} else if (provider === 'SimplifyVFD') {
				// SimplifyVFD format
				const cust = payload.customer || {};
				normalized.customer = {
					name: cust.name || '',
					id_type: cust.identificationType || '',
					id_value: cust.identificationNumber || ''
				};

				normalized.items = (payload.items || []).map(item => ({
					name: item.description || '',
					qty: item.quantity || 0,
					unit_price: item.unitAmount || 0,
					tax_code: item.taxType || 'STANDARD',
					amount: (item.unitAmount || 0) * (item.quantity || 0)
				}));

				const pmt = (payload.payments || [])[0] || {};
				normalized.payment = {
					type: pmt.type || 'INVOICE',
					amount: pmt.amount || 0
				};

				normalized.total = normalized.items.reduce((sum, item) => sum + item.amount, 0);
			}
		} catch (e) {
			console.error('Error normalizing payload:', e);
		}

		return normalized;
	},

	/**
	 * Get ID type label
	 */
	id_type_label: function(id_type) {
		const labels = {
			'1': 'TIN',
			'2': 'Driving License',
			'3': 'Voter ID',
			'4': 'Passport',
			'5': 'NID',
			'6': 'Other',
			'TAX_IDENTIFICATION_NUMBER': 'TIN',
			'DRIVING_LICENCE': 'Driving License',
			'VOTERS_NUMBER': 'Voter ID',
			'TRAVEL_DOCUMENT': 'Passport',
			'NATIONAL_ID': 'NID',
			'NIL': 'None'
		};
		return labels[id_type] || id_type || '-';
	},

	/**
	 * Get tax code label
	 */
	tax_code_label: function(code) {
		const labels = {
			'A': '18%',
			'B': 'Special',
			'C': 'Zero',
			'D': 'Relief',
			'E': 'Exempt',
			'1': '18%',
			'2': 'Special',
			'3': 'Zero',
			'4': 'Relief',
			'5': 'Exempt'
		};
		return labels[code] || code || '18%';
	},

	/**
	 * Submit receipt to TRA
	 */
	submit_receipt: function(frm) {
		frappe.call({
			method: 'tanzania.efd.utils.submit_efd_receipt',
			args: {
				invoice_name: frm.doc.name,
				preview: false
			},
			freeze: true,
			freeze_message: __('Submitting to TRA...'),
			callback: function(r) {
				if (r.message && r.message.success) {
					frappe.show_alert({
						message: __('EFD receipt submitted successfully!'),
						indicator: 'green'
					});
					frm.reload_doc();
				} else {
					frappe.msgprint({
						title: __('EFD Submission Failed'),
						message: r.message ? r.message.message : __('Unknown error'),
						indicator: 'red'
					});
					frm.reload_doc();
				}
			}
		});
	},

	/**
	 * Show status indicator
	 */
	show_status_indicator: function(frm) {
		if (!frm.doc.efd_status || frm.doc.efd_status === 'Not Sent') return;

		const indicators = {
			'Pending': 'orange',
			'Success': 'green',
			'Failed': 'red'
		};

		const color = indicators[frm.doc.efd_status] || 'grey';
		frm.dashboard.add_indicator(__('EFD: {0}', [frm.doc.efd_status]), color);
	}
};
