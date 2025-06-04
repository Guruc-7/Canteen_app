# Copyright (c) 2025, anonymous and contributors
# For license information, please see license.txt

# import frappe
# import frappe
# from frappe.model.document import Document

# class Payment(Document):
#     def on_submit(self):
#         if self.status == "Paid" and self.food_order:
#             frappe.db.set_value("Food Order", self.food_order, "status", "Delivered")
#             frappe.msgprint(f"Food Order {self.food_order} ")
import frappe
from frappe.model.document import Document
from frappe import _

class Payment(Document):
    def before_submit(self):
        if self.food_order:
            food_order = frappe.get_doc("Food Order", self.food_order)

            if self.amount_paid == 0:
                frappe.db.set_value("Food Order", self.food_order, "status", "Unpaid")
                frappe.throw(_("Your Order Is UnPaid"))

            elif 0 < self.amount_paid < food_order.total_amount:
                frappe.db.set_value("Food Order", self.food_order, "status", "Partially Paid")
                frappe.throw(_("You Must Pay Full Amount"))

            elif self.amount_paid == food_order.total_amount:
                frappe.db.set_value("Food Order", self.food_order, "status", "Delivered")

            elif self.amount_paid > food_order.total_amount:
                frappe.throw(_("Amount Paid cannot be more than Total Amount of the Food Order."))







