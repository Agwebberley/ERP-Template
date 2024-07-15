import django
from django.core.management.base import BaseCommand
from core.aws_utils import get_listeners, get_or_create_topic, get_channels
from importlib import import_module
from django.apps import apps
from django.conf import settings
import json
import boto3

class Command(BaseCommand):
    help = 'Run SQS worker'
    
    def handle(self, *args, **kwargs):
        django.setup()  # Ensure Django is fully initialized
        print("SQSWorker: Starting worker")
        self.sqs_client = boto3.client('sqs', region_name=settings.AWS_REGION)
        self.sns_client = boto3.client('sns', region_name=settings.AWS_REGION)
        for app_config in apps.get_app_configs():
            try:
                import_module(f'{app_config.name}.listeners')
                self.stdout.write(self.style.SUCCESS(f'Loaded listeners for {app_config.name}'))
            except ImportError:
                pass

        self.process_messages()

    def process_messages(self):
        while True:
            for channel in get_channels():
                queue_url = self.get_or_create_queue(channel)
                if queue_url:
                    self.poll_queue(queue_url)

    def get_or_create_queue(self, channel):
        try:
            queue_name = f"{channel}_queue"
            response = self.sqs_client.create_queue(QueueName=queue_name)
            queue_url = response['QueueUrl']
            queue_arn = self.sqs_client.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=['QueueArn']
            )['Attributes']['QueueArn']

            topic_arn = get_or_create_topic(channel)
            if topic_arn:
                self.sqs_client.set_queue_attributes(
                    QueueUrl=queue_url,
                    Attributes={
                        'Policy': json.dumps({
                            "Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Effect": "Allow",
                                    "Principal": "*",
                                    "Action": "sqs:SendMessage",
                                    "Resource": queue_arn,
                                }
                            ]
                        })
                    }
                )

                self.sns_client.subscribe(
                    TopicArn=topic_arn,
                    Protocol='sqs',
                    Endpoint=queue_arn
                )

            return queue_url
        except Exception as e:
            print(f"Error creating/getting SQS queue {channel}: {e}")
            return None

    def poll_queue(self, queue_url):
        messages = self.sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20
        )

        if 'Messages' in messages:
            for message in messages['Messages']:
                body = message['Body']
                self.process_message(body)
                self.sqs_client.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )

    def process_message(self, data):
        try:
            message_data = json.loads(data)
            message_data = json.loads(message_data['Message'])
            self.stdout.write(self.style.SUCCESS(f"Processing message: {message_data}"))
            channel = message_data.get('channel')
            action = message_data.get('action')
            serialized_data = message_data.get('data')
            self.stdout.write(self.style.SUCCESS(f"Processing message: {channel} - {action}"))

            listeners = get_listeners(channel)
            listeners += get_listeners("*")
            for listener in listeners:
                listener(channel, action, serialized_data)
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Failed to decode JSON: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error processing message: {e}"))
