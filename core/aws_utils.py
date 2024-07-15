import boto3
from django.conf import settings

sns_client = boto3.client("sns", region_name=settings.AWS_REGION)
sqs_client = boto3.client("sqs", region_name=settings.AWS_REGION)


def get_or_create_topic(channel):
    try:
        response = sns_client.create_topic(Name=channel)
        return response["TopicArn"]
    except Exception as e:
        print(f"Error creating/getting SNS topic {channel}: {e}")
        return None


def publish_event(channel, message):
    topic_arn = get_or_create_topic(channel)
    if topic_arn:
        sns_client.publish(TopicArn=topic_arn, Message=message)


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


def get_channels():
    return listeners.keys()
