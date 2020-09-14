
from django.utils import timezone
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from sms.models import Message, PhoneBook
from sms.at_service import send_sms
from sms.serializers import MessageSerializer


class MessageViewset(viewsets.ViewSet):

    def create(self, request):
        
        serializer = MessageSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"details": serializer.errors, "code": 400}, status=status.HTTP_400_BAD_REQUEST)

        at_response = send_sms(serializer.validated_data)

        # Response from AT contains a recipients key if it was succesful
        if at_response["SMSMessageData"]["Recipients"]:
            receiver = serializer.validated_data["receiver"]
            sender = serializer.validated_data["sender"]

            Message.objects.create(
                message=serializer.validated_data.get("message"),
                sender=serializer.validated_data.get("sender"),
                receiver=serializer.validated_data.get("receiver"),
                at_id=at_response["SMSMessageData"]["Recipients"][0]["messageId"],
                status=at_response["SMSMessageData"]["Recipients"][0]["status"]
            )

            return Response(
                {
                    "details": "Success",
                    "status": at_response["SMSMessageData"]["Recipients"][0]["status"],
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"details": at_response["SMSMessageData"].get("Message")},
                status=status.HTTP_400_BAD_REQUEST,
            ) 

    def list(self, request):

        self.phoneNumber = self.request.GET.get("phoneNumber", None)

        queryset = Message.objects.values().order_by("logged_at")

        if self.phoneNumber:
            from django.db.models import Q

            queryset = queryset.filter(
                Q(receiver=self.phoneNumber) | Q(sender=self.phoneNumber)
            )

        return Response({"details": queryset}, status=status.HTTP_200_OK)
       
    @action(methods=["POST"], detail=False)
    def incomingCallback(self, request):

        payload = request.data.dict()
        
        if not PhoneBook.objects.filter(phone_number=payload["from"]).exists():

            payload = {
                'message': 'Unfortunately, you texted a wrong number',
                'receiver': payload['from'],
                'sender': payload['to']
            }
            send_sms(payload)

            return Response(status=status.HTTP_202_ACCEPTED)
        
        else:

            Message.objects.create(
                receiver=payload["to"],
                sender=payload["from"],
                message=payload["text"],
                at_id=payload["id"],
                status="INBOX",
            )

            return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=["POST"], detail=False)
    def deliveryCallback(self, request):

        payload = request.data.dict()

        message = Message.objects.filter(at_id=payload["id"]).values()

        if message:
            message.update(
                delivery=payload.get("status"),
                delivered_at=timezone.now(),
                failure_reason=payload.get("failureReason"),
            )

        return Response(status=status.HTTP_202_ACCEPTED)


