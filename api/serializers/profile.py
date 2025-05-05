from ..models import Profile
from .profile_attribute import ProfileAttributeItemSerializer
from .analyse import AnalyseItemSerializer

from rest_framework import serializers

class ProfileItemSerializer(serializers.Serializer):
    pass

class ProfileSerializer(serializers.ModelSerializer):
    """
        Serializer to transform JSON format to a Profile object
    """
    profileattribute_set = ProfileAttributeItemSerializer(read_only=True, many=True)
    class Meta:
        model = Profile
        fields = [
            'pk',
            'status',
            'createdAt',
            'profileattribute_set'
        ]