from ..models import ProfileAttribute
from rest_framework import serializers

class ProfileAttributeSerializer(serializers.ModelSerializer):
    """
        Serializer to transform an ProfileAttribute object
        to a JSON format
    """
    class Meta:
        model = ProfileAttribute
        fields = '__all__'