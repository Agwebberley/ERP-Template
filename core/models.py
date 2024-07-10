from django.db import models
from django.contrib.auth.models import Group, User
from core.redis_utils import publish_event

# Meta Models

class LogMessage(models.Model):
    message = models.TextField()
    level = models.CharField(max_length=255)

    def __str__(self):
        return self.message

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def log_message(cls, instance, action):
        message = f"{cls.__name__} {action}: {instance}"
        level = "INFO" if action == "created" else "WARNING"
        LogMessage.objects.create(message=message, level=level)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.log_message(self, "created")
            publish_event(self.__class__.__name__, f"created: {self}")
        else:
            self.log_message(self, "updated")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.log_message(self, "deleted")
        super().delete(*args, **kwargs)
    
    class Meta:
        abstract = True

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

