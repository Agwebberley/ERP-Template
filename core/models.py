import datetime
import json
from django.db import models
from django.contrib.auth.models import Group, User
from core.redis_utils import publish_event
from django.forms.models import model_to_dict


# Meta Models



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
        event_data = {
            "action": "deleted",
            "data": self.serialize()
        }
        publish_event(self.__class__.__name__, json.dumps(event_data))
        super().delete(*args, **kwargs)
    
    def serialize(self):
        def convert_to_serializable(value):
            if isinstance(value, datetime.datetime):
                return value.isoformat()
            elif isinstance(value, datetime.date):
                return value.isoformat()
            return value

        data = {}
        for field in self._meta.get_fields():
            if field.is_relation:
                if field.many_to_one:
                    data[field.name] = getattr(self, field.name).id
                elif field.many_to_many:
                    data[field.name] = [obj.id for obj in getattr(self, field.name).all()]
            else:
                data[field.name] = getattr(self, field.name)

        data = model_to_dict(self)
        # Convert all values to JSON serializable format
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
    name = models.CharField(max_length=255)
    pattern = models.CharField(max_length=255)
    action_type = models.CharField(max_length=255, choices=ACTION_TYPES, default='dropdown')
    # Enabled Pages
    enable_in_list = models.BooleanField(default=True)
    enable_in_detail = models.BooleanField(default=True)


    def __str__(self):
        return self.name

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

