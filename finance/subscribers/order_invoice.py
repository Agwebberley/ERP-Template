from finance.models import Invoice

def event_handler(data):
    if data['action'] == 'created':
        order = data['data']
        create_invoice(order)
    elif data['action'] == 'updated':
        order = data['data']
        create_invoice(order)
    elif data['action'] == 'deleted':
        order = data['data']
        delete_invoice(order)

def create_invoice(order):
    invoice = Invoice.objects.get_or_create(order=order)
    return invoice

def delete_invoice(order):
    invoice = Invoice.objects.get(order=order)
    invoice.status = 'CANCELLED'
    invoice.save()
    return invoice