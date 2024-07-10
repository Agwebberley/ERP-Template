from core.redis_utils import listener


@listener('Order')
def order_listener(action, data):
    from finance.subscribers.order_invoice import event_handler as order_invoice_event_handler

    order_invoice_event_handler(action, data)