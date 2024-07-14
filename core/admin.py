from django.contrib import admin
from .models import AppConfiguration, ModelConfiguration, FieldConfiguration, ModelAction
from .management.commands.fake_data import Command as FakeDataCommand

@admin.register(AppConfiguration)
class AppConfigurationAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(ModelConfiguration)
class ModelConfigurationAdmin(admin.ModelAdmin):
    list_display = ['app', 'model_name', 'enable_search', 'list_title']
    search_fields = ['model_name']
    list_filter = ['app']
    filter_horizontal = ['read_permission_groups', 'read_permission_users', 'write_permission_groups', 'write_permission_users']


@admin.register(FieldConfiguration)
class FieldConfigurationAdmin(admin.ModelAdmin):
    list_display = ['model', 'field_name', 'enable_in_list', 'enable_in_detail', 'enable_in_form', 'display_name']
    search_fields = ['field_name']
    list_filter = ['model']
    filter_horizontal = ['read_permission_groups', 'read_permission_users', 'write_permission_groups', 'write_permission_users']

@admin.register(ModelAction)
class ModelActionAdmin(admin.ModelAdmin):
    list_display = ['list_name', 'pattern', 'action_type']
    search_fields = ['list_name']
    list_filter = ['action_type']
