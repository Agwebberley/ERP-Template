from django.core.management.base import BaseCommand
import redis

class Command(BaseCommand):
    help = 'Test connection to Redis'

    def handle(self, *args, **options):
        # Update with your MemoryDB endpoint
        memorydb_endpoint = 'clustercfg.redis.ysnb0i.memorydb.us-west-2.amazonaws.com'
        port = 6379

        # Create a Redis connection
        r = redis.StrictRedis(
            host=memorydb_endpoint,
            port=port,
            ssl=True  # Set to False if not using SSL
        )

        try:
            # Ping the Redis server
            response = r.ping()
            if response:
                self.stdout.write(self.style.SUCCESS("Successfully connected to Redis"))
            else:
                self.stdout.write(self.style.ERROR("Failed to connect to Redis"))
            
            # Close the connection
            r.close()
        except redis.ConnectionError as e:
            self.stdout.write(self.style.ERROR(f"Connection error: {e}"))
            r.close()
