// Copyright (c) 2024, Navari Limited and contributors
// For license information, please see license.txt

frappe.query_reports["Statutory Payment Tracking"] = {
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
            "fieldname": "period",
            "label": __("Period (Month)"),
            "fieldtype": "Date",
            "reqd": 1,
            "default": frappe.datetime.month_start()
        },
        {
            "fieldname": "supplier_group",
            "label": __("Supplier Group"),
            "fieldtype": "Link",
            "options": "Supplier Group",
            "default": "Government"
        }
    ],
    "onload": function (report) {
        // Auto-set the end date if period changes
    }
};
