// Copyright (c) 2025, anonymous and contributors
// For license information, please see license.txt
// Copyright (c) 2025, anonymous and contributors
// For license information, please see license.txt

frappe.ui.form.on("Food Order", {
    order_date: function(frm) {
        const orderDate = new Date(frm.doc.order_date);
        const today = new Date();
        orderDate.setHours(0, 0, 0, 0);
        today.setHours(0, 0, 0, 0);

        if (orderDate < today) {
            frappe.msgprint(__('Order date cannot be before today.'));
            frm.set_value('order_date', '');
        }
    },

    on_submit: function(frm) {
        frm.set_value("status", "Confirmed");
        frappe.msgprint(__('Your order has been placed successfully.'));
    },

    refresh: function(frm) {
        // Add "Make Payment" button
        frm.add_custom_button(__('Make Payment'), function () {
            frappe.call({
                method: 'canteen_app.canteen_app.doctype.food_order.food_order.make_payment',
                args: { food_order: frm.doc.name },
                callback: function (r) {
                    if (r.message) {
                        frappe.set_route('Form', 'Payment', r.message);
                    }
                }
            });
        });

        // Add "Create Pickup Order" button
frm.add_custom_button(__('Create'), function () {
    frappe.call({
        method: 'canteen_app.doctype.food_order.food_order.create_pickup_order',
        args: { food_order_name: frm.doc.name },
        callback: function (r) {
            if (r.message) {
                frappe.set_route('Form', 'Pickup Order', r.message);
            }
        }
    });
});



        // Add "Update Order" button
        frm.add_custom_button('Update Order', () => {
            const field = frm.fields_dict['order_item'];
            if (field && field.grid) {
                field.$wrapper[0].scrollIntoView({ behavior: 'smooth' });
                field.grid.wrapper.find('.grid-body .grid-empty').hide();
                field.grid.wrapper.find('.grid-body').show();

                if (field.grid.grid_rows?.length > 0) {
                    field.grid.grid_rows[0].toggle_view();
                } else {
                    field.grid.add_new_row();
                }

                if (frm.doc.docstatus === 1) {
                    field.grid.grid_rows.forEach(row => {
                        row.toggle_editable('menu_item', true);
                        row.toggle_editable('quantity', true);
                    });

                    field.grid.on('grid-add-row', function() {
                        const last_row = field.grid.grid_rows.at(-1);
                        if (last_row) {
                            last_row.toggle_editable('menu_item', true);
                            last_row.toggle_editable('quantity', true);
                        }
                    });
                }
            }
        });
    }
});

// Child table event handlers
frappe.ui.form.on('Food Order Item', {
    menu_item: function(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        if (row.menu_item) {
            frappe.db.get_doc('Menu Items', row.menu_item)
                .then(doc => {
                    frappe.model.set_value(cdt, cdn, 'rate', doc.price);
                    let quantity = row.quantity || 1;
                    frappe.model.set_value(cdt, cdn, 'amount', quantity * doc.price);
                });
        }
    },

    quantity: function(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
    },

    rate: function(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
    }
});

// Helper functions
function calculate_amount(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    row.amount = (row.quantity || 0) * (row.rate || 0);
    frm.refresh_field('order_item');
    calculate_total(frm);
}

function calculate_total(frm) {
    let total = 0;
    frm.doc.order_item.forEach(row => {
        total += row.amount || 0;
    });
    frm.set_value('total_amount', total);
}

// // Optional: Make child fields read-only
// function set_child_table_read_only(frm) {
//     frm.fields_dict['order_item'].grid.get_field('quantity').set_df_property('read_only', 1);
//     frm.fields_dict['order_item'].grid.get_field('rate').set_df_property('read_only', 1);
//     frm.fields_dict['order_item'].grid.get_field('amount').set_df_property('read_only', 1);
// }
