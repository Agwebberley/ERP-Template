from django import forms
from django.apps import apps
from django.urls import get_resolver, get_urlconf
from core.models import AppConfiguration, ModelConfiguration, FieldConfiguration

def get_app_config(app_name):
    try:
        return AppConfiguration.objects.get(name=app_name)
    except AppConfiguration.DoesNotExist:
        return None

def get_model_config(app_name, model_name):
    try:
        app_config = get_app_config(app_name)
        return ModelConfiguration.objects.get(app=app_config, model_name=model_name)
    except ModelConfiguration.DoesNotExist:
        return None

def get_field_configs(app_name, model_name):
    model_config = get_model_config(app_name, model_name)
    if model_config:
        return FieldConfiguration.objects.filter(model=model_config)
    return []

def get_enabled_fields(app_name, model_name, user, view_type='list'):
    field_configs = get_field_configs(app_name, model_name)
    enabled_fields = []
    for field_config in field_configs:
        if view_type == 'list' and field_config.enable_in_list and user_has_field_read_permission(user, field_config):
            enabled_fields.append(field_config.field_name)
        elif view_type == 'show' and field_config.enable_in_show and user_has_field_read_permission(user, field_config):
            enabled_fields.append(field_config.field_name)
    return enabled_fields

def user_has_model_read_permission(user, model_config):
    if user.is_superuser:
        return True
    if model_config.read_permission_users.filter(id=user.id).exists():
        return True
    if model_config.read_permission_groups.filter(id__in=user.groups.values_list('id', flat=True)).exists():
        return True
    return False

def user_has_model_write_permission(user, model_config):
    if user.is_superuser:
        return True
    if model_config.write_permission_users.filter(id=user.id).exists():
        return True
    if model_config.write_permission_groups.filter(id__in=user.groups.values_list('id', flat=True)).exists():
        return True
    return False

def user_has_field_read_permission(user, field_config):
    if field_config.inherit_permissions:
        return user_has_model_read_permission(user, field_config.model)
    if user.is_superuser:
        return True
    if field_config.read_permission_users.filter(id=user.id).exists():
        return True
    if field_config.read_permission_groups.filter(id__in=user.groups.values_list('id', flat=True)).exists():
        return True
    return False

def user_has_field_write_permission(user, field_config):
    if field_config.inherit_permissions:
        return user_has_model_write_permission(user, field_config.model)
    if user.is_superuser:
        return True
    if field_config.write_permission_users.filter(id=user.id).exists():
        return True
    if field_config.write_permission_groups.filter(id__in=user.groups.values_list('id', flat=True)).exists():
        return True
    return False

def generate_dynamic_form(app_name, model_name, user):
    model_class = apps.get_model(app_label=app_name, model_name=model_name)
    config = get_model_config(app_name, model_name)
    enabled_fields = get_enabled_fields(app_name, model_name, user)

    class DynamicForm(forms.ModelForm):
        class Meta:
            model = model_class
            fields = enabled_fields

    return DynamicForm

def get_actions(app_name, model_name):
    model_config = get_model_config(app_name, model_name)
    actions = {'dropdown': [], 'button': []}
    # Seperate dropdown actions from button actions
    for action in model_config.actions.all():
        if action.action_type == 'dropdown':
            actions['dropdown'].append({'name': action.name, 'pattern': model_name.lower() + '-' + action.pattern})
        if action.action_type == 'button':
            actions['button'].append({'name': action.name, 'pattern': model_name.lower() + '-' + action.pattern})
    print(actions)
    return actions