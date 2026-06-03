from django.contrib import admin
from .models import School, Domain

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'schema_name', 'plan', 'is_active', 'created_on']
    list_filter  = ['plan', 'is_active']

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'tenant', 'is_primary']
