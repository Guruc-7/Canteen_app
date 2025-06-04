// Copyright (c) 2025, anonymous and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pickup Order', {
    refresh: function(frm) {
        if (!frm.doc.__islocal && frm.doc.status !== "Cancelled") {
            frm.add_custom_button(__('Make Payment'), function() {
                frappe.call({
                    method: 'canteen_app.canteen_app.doctype.pickup_order.pickup_order.make_payment',
                    args: {
                        pickup_order: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message) {
                            console.log(r.message);
                            frappe.set_route('Form', 'Payment', r.message);
                        }
                    }
                });
            });
        }
    },

    order_id: function(frm) {
        if (frm.doc.order_id) {
            frappe.call({
                method: 'canteen_app.api.get_food_order_details',
                args: {
                    order_id: frm.doc.order_id
                },
                callback: function(r) {
                    if (r.message) {
                        let food_order = r.message;
                        frm.clear_table('order_table');

                        (food_order.order_item || []).forEach(row => {
                            let child = frm.add_child('order_table');
                            child.menu_item = row.menu_item;
                            child.quantity = row.quantity;
                            child.rate = row.rate;
                            child.amount = row.amount;
                        });

                        frm.set_value('total_amount', food_order.total_amount);
                        frm.refresh_field('order_table');
                    }
                }
            });
        }
    }
});

