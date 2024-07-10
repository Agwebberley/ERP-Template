from django.conf import settings
import redis

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

def publish_event(channel, message):
    redis_client.publish(channel, message)

def subscribe_to_channel(channel):
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)
    return pubsub

listeners = {}

def listener(channel):
    def decorator(func):
        if channel not in listeners:
            listeners[channel] = []
        listeners[channel].append(func)
        return func
    return decorator

def get_listeners(channel):
    return listeners.get(channel, [])