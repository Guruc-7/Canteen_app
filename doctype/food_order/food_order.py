import frappe
from frappe import _
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


