from rest_framework import serializers, status

import requests
from requests.exceptions import MissingSchema, ConnectionError

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

    def validate(self, data):
        data = super().validate(data)

        try:
            requests.post(data['url'])
        except ConnectionError:
            raise serializers.ValidationError({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Connection Error",
                "details":[
                    {
                        "field": "url",
                        "error": "We couldn't connect to the given url. Please make sure it is correct."
                    }
                ]
            })
        except MissingSchema:
            raise serializers.ValidationError({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Missing Schema",
                "details":[
                    {
                        "field": "url",
                        "error": "This is not an url. Perhaps you meant https://%s ?" % (data['url'])
                    }
                ]
            })