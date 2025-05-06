from ..models import Profile
from .profile_attribute import ProfileAttributeItemSerializer
from .analyse import AnalyseItemSerializer
from .attribute import AttributeItemSerializer
from .document import DocumentItemSerializer

from rest_framework import serializers

class ProfileItemSerializer(serializers.ModelSerializer):
    """
        Serializer to transform a Profile object to JSON format
    """
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    externalReference = serializers.CharField(read_only=True)
    profileattribute_set = ProfileAttributeItemSerializer(read_only=True, many=True)
    document_set = DocumentItemSerializer(read_only=True, many=True)
    last_analyse = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'createdAt',
            'updatedAt',
            'status',
            'externalReference',
            'profileattribute_set',
            'document_set',
            'last_analyse'
        ]

    def get_last_analyse(self, obj):
        analyse = obj.analyse_set.order_by('-id')[:1].first()
        if analyse:
            return {
                'score' : analyse.score,
                'status' : analyse.status,
                'details' : analyse.details,
                'version' : analyse.version
            }
        return None
    

class ProfileSerializer(serializers.ModelSerializer):
    """
        Serializer to transform JSON format to a Profile object
    """
    profileattribute_set = ProfileAttributeItemSerializer(read_only=True, many=True)
    status = serializers.CharField(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)
    pk = serializers.IntegerField(read_only=True)
    externalReference = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = [
            'pk',
            'status',
            'createdAt',
            'profileattribute_set',
            'externalReference'
        ]