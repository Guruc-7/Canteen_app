# Copyright (c) 2025, anonymous and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PickupOrder(Document):
    def before_save(self):
        if not self.status:
            self.status = "Pickup"

        food_order_status = frappe.db.get_value("Food Order", self.food_order, "status")
        if food_order_status == "Cancelled":
            self.status = "Cancelled"

@frappe.whitelist()
def get_food_order_details(order_id):
    order = frappe.get_doc("Food Order", order_id)
    return {
        "order_item": order.order_item,
        "total_amount": order.total_amount
    }

@frappe.whitelist()
def make_payment(pickup_order):
    pickup_order = frappe.get_doc("Pickup Order", pickup_order)

    payment = frappe.new_doc("Payment")
    payment.food_order = pickup_order.food_order  # corrected from order_id
    payment.amount_paid = pickup_order.total_amount
    payment.insert(ignore_permissions=True)

    return payment.name

