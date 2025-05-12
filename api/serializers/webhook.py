from rest_framework import serializers

from ..models import Webhook

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