from rest_framework import serializers

from ..models import Webhook

class WebhookItemSerializer(serializers.Serializer):
    url = serializers.CharField(read_only=True)

class WebhookSerializer(serializers.ModelSerializer):
    """
        Serializer to transform JSON to Webhook object.
    """
    class Meta:
        model = Webhook
        fields = [
            'pk',
            'url',
        ]
