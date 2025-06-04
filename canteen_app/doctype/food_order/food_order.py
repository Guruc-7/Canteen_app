# Copyright (c) 2025, anonymous and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

# FoodOrder class with stock availability check
class FoodOrder(Document):
    def validate(self):
        frappe.msgprint("hi")
        food_order = self.name
        for item in self.order_item:
            menu_item = item.menu_item
            avaliability = frappe.db.get_value("Menu Items", {"name": menu_item}, "avaliability")
            if avaliability == 0:
                frappe.throw("Stock Not Available")

# Payment class with validation
class Payment(Document):
    def validate(self):
        if self.food_order:
            food_order = frappe.get_doc("Food Order", self.food_order)
            if self.amount_paid > food_order.total_amount:
                frappe.throw(_("Amount Paid cannot exceed the Food Order's Total Amount ({0}).").format(food_order.total_amount))

# Whitelisted method to make payment
@frappe.whitelist()
def make_payment(food_order):
    food_order_doc = frappe.get_doc("Food Order", food_order)

    payment = frappe.new_doc("Payment")
    payment.food_order = food_order_doc.name
    payment.amount_paid = food_order_doc.total_amount
    payment.payment_date = frappe.utils.nowdate()
    payment.insert(ignore_permissions=True)

    frappe.msgprint(_("Payment {0} created.").format(payment.name))
    return payment.name

@frappe.whitelist()
def create_pickup_order(food_order_name):
    food_order = frappe.get_doc("Food Order", food_order_name)

    pickup = frappe.new_doc("Pickup Order")
    pickup.food_order = food_order.name
    pickup.customer = food_order.customer
    pickup.status = "Pickup" 

    total_amount = 0
    for item in food_order.order_item:
        pickup.append("pickup_order", {
            "menu_item": item.menu_item,
            "quantity": item.quantity,
            "price": item.rate,
            "amount": item.amount
        })
        total_amount += item.amount

    pickup.total_amount = total_amount

    pickup.insert(ignore_permissions=True)
    return pickup.name




# @frappe.whitelist()
# def create_pickup_order(food_order_name):
#     # Get the Food Order document
#     food_order = frappe.get_doc("Food Order", food_order_name)

#     # Create new Pickup Order and set fields from Food Order
#     pickup = frappe.new_doc("Pickup Order")
#     pickup.food_order = food_order.name
#     pickup.customer = food_order.customer  # example field
#     pickup.order_date = food_order.order_date  # example field

#     # If Pickup Order has child table, you can copy rows too
#     for item in food_order.order_item:
#         pickup.append("pickup_items", {
#             "menu_item": item.menu_item,
#             "quantity": item.quantity,
#             "rate": item.rate,
#             "amount": item.amount
#         })

#     pickup.insert()
#     frappe.db.commit()
#     return pickup.name












