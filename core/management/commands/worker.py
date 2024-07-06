import redis
from rq import Worker, Queue, Connection
from django.conf import settings
from django.core.management.base import BaseCommand

# worker_command.py


class Command(BaseCommand):
    help = 'Starts a worker for processing RQ jobs'

    def handle(self, *args, **options):
        listen = ['default']
        conn = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        
        with Connection(conn):
            worker = Worker(list(map(Queue, listen)))
            worker.work()
