from ..models import Profile
from .profile_attribute import ProfileAttributeSerializer

from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    """
        Serializer to transform an ProfileAttribute object
        to a JSON format
    """
    profileattribute_set = ProfileAttributeSerializer(read_only=True, many=True)
    class Meta:
        model = Profile
        fields = [
            'pk',
            'status',
            'createdAt',
            'profileattribute_set'
        ]