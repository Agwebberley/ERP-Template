from core.redis_utils import listener

@listener('Part')
def order_listener(data):
    print(f'Order received: {data}')