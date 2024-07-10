from core.redis_utils import get_listeners
from importlib import import_module
from django.apps import apps
from django.core.management.base import BaseCommand
import redis
from django.conf import settings

class Command(BaseCommand):
    help = 'Run Redis worker'

    def handle(self, *args, **kwargs):
        r = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])
        pubsub = r.pubsub()
        pubsub.psubscribe('*')  # Subscribe to all channels

        for app_config in apps.get_app_configs():
            try:
                import_module(f'{app_config.name}.listeners')
                print(f'Loaded listeners for {app_config.name}')
            except ImportError:
                pass

        for message in pubsub.listen():
            if message['type'] == 'pmessage':
                channel = message['channel'].decode('utf-8')
                data = message['data']
                print(f'Channel: {channel}, Data: {data}')
                self.process_message(channel, data)

    def process_message(self, channel, data):
        listeners = get_listeners(channel)
        for listener in listeners:
            listener(data)
