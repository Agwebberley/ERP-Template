from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

@receiver(post_save)
def your_signal(sender, instance, created, **kwargs):
    pass
