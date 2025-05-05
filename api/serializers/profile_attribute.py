from ..models import ProfileAttribute
from .attribute import AttributeItemSerializer

from rest_framework import serializers

class ProfileAttributeSerializer(serializers.ModelSerializer):
    """
        Serializer to transform an ProfileAttribute object
        to a JSON format
    """
    attribute = AttributeItemSerializer(read_only=True)
    class Meta:
        model = ProfileAttribute
        fields = [
            'attribute',
            'value'
        ]