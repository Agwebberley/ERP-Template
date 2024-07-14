import datetime
from decimal import Decimal
import json
from django.db import models
from django.contrib.auth.models import Group, User
from core.aws_utils import publish_event
from django.forms.models import model_to_dict


# Meta Models
class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = BaseModelManager()
    all_objects = models.Manager()  # Manager that includes deleted objects

    def save(self, *args, **kwargs):
        if not self.pk:
            event_data = {
                "action": "created",
                "data": self.serialize()
            }
            publish_event(self.__class__.__name__, json.dumps(event_data))
        else:
            event_data = {
                "action": "updated",
                "data": self.serialize()
            }
            publish_event(self.__class__.__name__, json.dumps(event_data))
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        event_data = {
            "action": "deleted",
            "data": self.serialize()
        }
        publish_event(self.__class__.__name__, json.dumps(event_data))
        self.save()

    def serialize(self):
        def convert_to_serializable(value):
            if isinstance(value, datetime.datetime):
                return value.isoformat()
            elif isinstance(value, datetime.date):
                return value.isoformat()
            elif isinstance(value, Decimal):
                return float(value)
            return value

        data = model_to_dict(self)
        data = {k: convert_to_serializable(v) for k, v in data.items()}

        return data

    class Meta:
        abstract = True


class LogMessage(BaseModel):
    channel = models.CharField(max_length=255, blank=True, null=True)
    action = models.CharField(max_length=255, blank=True, null=True)
    message = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.channel} - {self.action}"

class ModelAction(models.Model):
    ACTION_TYPES = {
        ('dropdown', 'Dropdown'),
        ('button', 'Button')
    }
    list_name = models.CharField(max_length=255)
    detail_name = models.CharField(max_length=255, null=True, blank=True)
    pattern = models.CharField(max_length=255)
    action_type = models.CharField(max_length=255, choices=ACTION_TYPES, default='dropdown')
    # Enabled Pages
    enable_in_list = models.BooleanField(default=True)
    enable_in_detail = models.BooleanField(default=True)
    include_pk = models.BooleanField(default=True)


    def __str__(self):
        return self.list_name

class AppConfiguration(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    navigation_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ModelConfiguration(models.Model):
    app = models.ForeignKey(AppConfiguration, related_name='models', on_delete=models.CASCADE)
    model_name = models.CharField(max_length=255)
    enable_search = models.BooleanField(default=True)
    list_title = models.CharField(max_length=255, blank=True, null=True)
    default_sort_by = models.CharField(max_length=255, blank=True, null=True)
    navigation_enabled = models.BooleanField(default=True)
    list_url = models.CharField(max_length=255, blank=True, null=True)
    # Views
    actions = models.ManyToManyField(ModelAction, related_name='models', blank=True)
    # Permissions
    read_permission_groups = models.ManyToManyField(Group, related_name='read_model_permissions', blank=True)
    read_permission_users = models.ManyToManyField(User, related_name='read_model_permissions', blank=True)
    write_permission_groups = models.ManyToManyField(Group, related_name='write_model_permissions', blank=True)
    write_permission_users = models.ManyToManyField(User, related_name='write_model_permissions', blank=True)

    def __str__(self):
        return f"{self.app.name} - {self.model_name}"


class FieldConfiguration(models.Model):
    model = models.ForeignKey(ModelConfiguration, related_name='fields', on_delete=models.CASCADE)
    field_name = models.CharField(max_length=255)
    enable_in_list = models.BooleanField(default=True)
    enable_in_detail = models.BooleanField(default=True)
    enable_in_form = models.BooleanField(default=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    inherit_permissions = models.BooleanField(default=True)
    read_permission_groups = models.ManyToManyField(Group, related_name='read_field_permissions', blank=True)
    read_permission_users = models.ManyToManyField(User, related_name='read_field_permissions', blank=True)
    write_permission_groups = models.ManyToManyField(Group, related_name='write_field_permissions', blank=True)
    write_permission_users = models.ManyToManyField(User, related_name='write_field_permissions', blank=True)

    def __str__(self):
        return f"{self.model.model_name} - {self.field_name}"

