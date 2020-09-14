from django.conf import settings
import africastalking

def send_sms(payload: str):

    username = settings.AFRICASTALKING["username"]  # use 'sandbox' for development in the test environment
    api_key = settings.AFRICASTALKING["key"]  # use your sandbox app API key for development in the test environment
    
    africastalking.initialize(username, api_key)

    # Initialize a service e.g. SMS
    sms = africastalking.SMS

    recipients = [payload.get('receiver')]
    sender = payload.get('sender')
    message = payload.get('message')

    return sms.send(message, recipients, sender)
