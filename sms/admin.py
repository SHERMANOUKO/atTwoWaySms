from django.contrib import admin

# Register your models here.
from sms.models import PhoneBook, Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = ("sender", "receiver", "message")


@admin.register(PhoneBook)
class PhoneBookAdmin(admin.ModelAdmin):

    list_display = ("name", "phone_number")

