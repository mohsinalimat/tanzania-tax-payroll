frappe.ui.form.on('EFD Settings', {
	refresh: function(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__('Fetch Device Info'), function() {
				frm.call({
					method: 'fetch_device_info',
					doc: frm.doc,
					freeze: true,
					freeze_message: __('Fetching device info from TRA...'),
					callback: function(r) {
						frm.reload_doc();
					}
				});
			});

			frm.add_custom_button(__('Test Connection'), function() {
				frm.call({
					method: 'test_connection',
					doc: frm.doc,
					freeze: true,
					freeze_message: __('Testing connection...'),
					callback: function(r) {
						// Response handled in Python
					}
				});
			});
		}
	},

	provider: function(frm) {
		// Clear device info when provider changes
		if (frm.doc.provider) {
			frm.set_value('device_serial', '');
			frm.set_value('tin', '');
			frm.set_value('vrn', '');
			frm.set_value('last_response', '');
		}
	}
});
