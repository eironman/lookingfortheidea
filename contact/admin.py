from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Contact messages"""
    date_hierarchy = 'date'
    list_display = ('name', 'email', 'message', 'date')