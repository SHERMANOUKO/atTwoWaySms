from rest_framework import serializers

class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    sender = serializers.CharField()
    receiver = serializers.CharField()

