from django import forms
from django.apps import apps
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


def get_enabled_fields(app_name, model_name, user, view_type="list", properties=True):
    model = apps.get_model(app_label=app_name, model_name=model_name)
    field_configs = get_field_configs(app_name, model_name)
    model_field_names = [field.name for field in model._meta.get_fields()]
    enabled_fields = []
    for field_config in field_configs:
        if field_config.field_name in model_field_names:
            field = model._meta.get_field(field_config.field_name)
            if not (field.auto_created or field.one_to_one or field.many_to_many):
                if (
                    view_type == "list"
                    and field_config.enable_in_list
                    and user_has_field_read_permission(user, field_config)
                ):
                    enabled_fields.append(field_config.field_name)
                elif (
                    view_type == "detail"
                    and field_config.enable_in_detail
                    and user_has_field_read_permission(user, field_config)
                ):
                    enabled_fields.append(field_config.field_name)
                elif (
                    view_type == "form"
                    and field_config.enable_in_form
                    and user_has_field_write_permission(user, field_config)
                ):
                    enabled_fields.append(field_config.field_name)
    if view_type != "form" and properties:
        properties = [
            prop for prop in dir(model) if isinstance(getattr(model, prop), property)
        ]
        if "pk" in properties:
            properties.pop(properties.index("pk"))
        enabled_fields += properties

    if "is_deleted" in enabled_fields:
        enabled_fields.pop(enabled_fields.index("is_deleted"))
    return enabled_fields


def user_has_model_read_permission(user, model_config):
    if user.is_superuser:
        return True
    if model_config.read_permission_users.filter(id=user.id).exists():
        return True
    if model_config.read_permission_groups.filter(
        id__in=user.groups.values_list("id", flat=True)
    ).exists():
        return True
    return False


def user_has_model_write_permission(user, model_config):
    if user.is_superuser:
        return True
    if model_config.write_permission_users.filter(id=user.id).exists():
        return True
    if model_config.write_permission_groups.filter(
        id__in=user.groups.values_list("id", flat=True)
    ).exists():
        return True
    return False


def user_has_field_read_permission(user, field_config):
    if field_config.inherit_permissions:
        return user_has_model_read_permission(user, field_config.model)
    if user.is_superuser:
        return True
    if field_config.read_permission_users.filter(id=user.id).exists():
        return True
    if field_config.read_permission_groups.filter(
        id__in=user.groups.values_list("id", flat=True)
    ).exists():
        return True
    return False


def user_has_field_write_permission(user, field_config):
    if field_config.inherit_permissions:
        return user_has_model_write_permission(user, field_config.model)
    if user.is_superuser:
        return True
    if field_config.write_permission_users.filter(id=user.id).exists():
        return True
    if field_config.write_permission_groups.filter(
        id__in=user.groups.values_list("id", flat=True)
    ).exists():
        return True
    return False


def generate_dynamic_form(app_name, model_name, user, instance=None):
    model_class = apps.get_model(app_label=app_name, model_name=model_name)
    enabled_fields = get_enabled_fields(app_name, model_name, user, view_type="form")

    class DynamicForm(forms.ModelForm):
        class Meta:
            model = model_class
            fields = enabled_fields

            def __init__(self, *args, **kwargs):
                super(DynamicForm, self).__init__(*args, **kwargs)

    return DynamicForm


def get_actions(app_name, model_name, view_type="list"):
    model_config = get_model_config(app_name, model_name)
    if view_type == "list":
        actions = {"dropdown": [], "button": []}
    elif view_type == "detail":
        actions = []
    # Seperate dropdown actions from button actions
    for action in model_config.actions.all():
        if view_type == "list" and action.enable_in_list:
            if action.action_type == "dropdown":
                actions["dropdown"].append(
                    {
                        "name": action.list_name,
                        "pattern": model_name.lower() + "-" + action.pattern,
                    }
                )
            if action.action_type == "button":
                actions["button"].append(
                    {
                        "name": action.list_name,
                        "pattern": model_name.lower() + "-" + action.pattern,
                    }
                )
        elif view_type == "detail" and action.enable_in_detail:
            actions.append(
                {
                    "name": action.detail_name,
                    "pattern": model_name.lower() + "-" + action.pattern,
                    "include_pk": action.include_pk,
                }
            )
    return actions


def generate_inline_formset(app_label, parent_model, child_model, model_name, user):
    return forms.inlineformset_factory(
        parent_model,
        child_model,
        form=generate_dynamic_form(app_label, model_name, user),
        extra=1,
    )
