from django.db import models
from django.utils import timezone


class ContactMessage(models.Model):
    """Messages sent with the contact form"""
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True)
    message = models.TextField()
    date = models.DateTimeField('sent date', default=timezone.now)
