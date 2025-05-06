from ..models import ProfileAttribute
from .attribute import AttributeItemSerializer

from rest_framework import serializers

class ProfileAttributeItemSerializer(serializers.Serializer):
    """
        Serializer to transform a ProfileAttribute to JSON format 
    """
    attribute = AttributeItemSerializer(read_only=True)
    value = serializers.CharField(read_only=True)

class ProfileAttributeSerializer(serializers.ModelSerializer):
    """
        Serializer to transform Json to a ProfileAttribute object
    """
    class Meta:
        model = ProfileAttribute
        fields = '__all__'


