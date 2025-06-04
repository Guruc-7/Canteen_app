import frappe

@frappe.whitelist()
def get_food_order_details(order_id):
    order = frappe.get_doc("Food Order", order_id)
    return {
        "order_item": order.order_item,
        "total_amount": order.total_amount
    }
