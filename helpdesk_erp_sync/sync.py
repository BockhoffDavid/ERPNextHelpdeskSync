
import frappe

def create_sales_order_for_ticket(doc, event):
    ticket = doc
    customer_email = ticket.email
    subject = ticket.subject or "Support Ticket"
    description = ticket.description or ""

    customer = frappe.db.get_value(
        "Customer",
        {"email_id": customer_email},
        ["name"],
    )

    if not customer:
        customer_name = customer_email.split("@")[0]
        customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": customer_name,
            "customer_type": "Individual",
            "email_id": customer_email
        }).insert(ignore_permissions=True).name

    sales_order = frappe.get_doc({
        "doctype": "Sales Order",
        "customer": customer,
        "transaction_date": frappe.utils.nowdate(),
        "items": [
            {
                "item_code": "Support",
                "description": f"Helpdesk Ticket: {subject}\n\n{description}",
                "qty": 1,
                "rate": 0
            }
        ],
        "delivery_date": frappe.utils.nowdate(),
        "order_type": "Service"
    })

    sales_order.insert(ignore_permissions=True)
    sales_order.submit()

    ticket.db_set("erpnext_sales_order", sales_order.name)
