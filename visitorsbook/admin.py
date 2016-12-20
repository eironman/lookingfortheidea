from django.contrib import admin
from .models import VisitorBookMessage


@admin.register(VisitorBookMessage)
class VisitorBookMessageAdmin(admin.ModelAdmin):
    """Publication in the visitor's book"""
    date_hierarchy = 'date'
    fields = ('name', 'message', 'date', 'image', 'image_tag')
    list_display = ('name', 'message', 'date', 'image_tag')
    readonly_fields = ('image_tag',)
