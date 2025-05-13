from ..models import Profile, Attribute
from .profile_attribute import ProfileAttributeItemSerializer
from .profile_attribute_document import ProfileAttributeDocumentItemSerializer

from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

class ProfileItemSerializer(serializers.ModelSerializer):
    """
        Serializer to transform a Profile object to JSON.
    """
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    externalReference = serializers.CharField(read_only=True)
    profileattribute_set = ProfileAttributeItemSerializer(read_only=True, many=True)
    document_set = ProfileAttributeDocumentItemSerializer(read_only=True, many=True)
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
        """
            Method to retrieve the last Analysis of a Profile.
        """
        analyse = obj.analysis_set.order_by('-id')[:1].first()
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
        Serializer to transform JSON to a Profile object.
    """
    attributes = serializers.DictField(write_only=True)
    profileattribute_set = ProfileAttributeItemSerializer(read_only=True, many=True)
    status = serializers.CharField(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)
    pk = serializers.IntegerField(read_only=True)
    externalReference = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Profile
        fields = [
            'pk',
            'status',
            'createdAt',
            'profileattribute_set',
            'externalReference',
            'attributes'
        ]

    def create(self, validated_data):
        validated_data.pop("attributes")
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.externalReference = validated_data.get('externalReference', instance.externalReference)
        return instance
    
    def validate(self, data):
        data = super().validate(data)
        
        required_attributes = Attribute.objects.filter(isRequired=True).exclude(category="document")
        for name, value in data['attributes'].items():
            required_attributes = required_attributes.exclude(name=name)
        
        if required_attributes:
            raise serializers.ValidationError({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Missing required attributes.",
                "details":[
                    {"error": "The following attributes are missing : %s" % (list(map(str, required_attributes)))}
                ]
            })

        return data

        
    