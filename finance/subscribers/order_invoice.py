from finance.models import Invoice
from orders.models import Order


def event_handler(action, data):
    if action == "created":
        create_invoice(data)
    elif action == "updated":
        create_invoice(data)
    elif action == "deleted":
        delete_invoice(data)


def create_invoice(order):
    order = Order.objects.get(id=order["id"])
    invoice = Invoice.objects.get_or_create(order=order)
    return invoice


def delete_invoice(order):
    order = Order.objects.get(id=order["id"])
    invoice = Invoice.objects.get_or_create(order=order)
    invoice.status = "CANCELLED"
    invoice.save()
    return invoice
