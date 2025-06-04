// Copyright (c) 2025, anonymous and contributors
// For license information, please see license.txt

frappe.ui.form.on("Payment", {
    on_submit: function(frm) {
        frappe.msgprint("Your payment was successful.");
    }
});
