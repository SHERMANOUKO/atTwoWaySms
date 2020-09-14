from rest_framework import routers

from sms import views as sms

router = routers.DefaultRouter()

router.register("sms", sms.MessageViewset, basename="sms")

