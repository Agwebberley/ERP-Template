from aws_utils import listener
from core.models import LogMessage 

@listener("*")
def log_message_listener(channel, action, data):
    LogMessage.objects.create(
        channel=channel,
        action=action,
        data=data
   )
    print(f"Logged message: {channel} - {action} - {data}")
