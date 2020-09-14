from django.db import models

# Create your models here.
class Message(models.Model):
    message = models.TextField()
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    at_id = models.CharField(max_length=100)
    status = models.CharField(null=True, blank=True, max_length=100)
    delivery = models.CharField(null=True, blank=True, max_length=100)
    logged_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    failure_reason = models.CharField(null=True, blank=True, max_length=100)

class PhoneBook(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
