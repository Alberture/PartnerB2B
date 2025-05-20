from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from ..models.profile_attribute_document import ProfileAttributeDocument
from ..models.attribute import Attribute

class ProfileDocumentSerializer(serializers.Serializer):
    """
        Serializer to transform a Profile object to JSON, copy of ProfileItemSerializer.
        it is mainly to avoid circular import.
    """
    pk = serializers.IntegerField(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    externalReference = serializers.CharField(read_only=True)

class ProfileAttributeDocumentItemSerializer(serializers.ModelSerializer):
    """
        Serializer to transform a ProfileAttributeDocument object to JSON format.
        Used to represent a ProfileAttributeDocument when retrieved.
    """
    profile = ProfileDocumentSerializer(read_only=True)
    file = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)
    downloadedAt = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    metadata = serializers.CharField(read_only=True)
    class Meta:
        model = ProfileAttributeDocument
        fields = [
            'profile',
            'file',
            'type',
            'downloadedAt',
            'status',
            'metadata',
        ]

class ProfileAttributeDocumentSerializer(serializers.ModelSerializer):
    """
        Serializer to transform JSON to a ProfileAttributeDocument object.
        Used to create ProfileAttributeDocument with the given data.
    """
    pk = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    downloadedAt = serializers.DateTimeField(read_only=True)
    file = serializers.FileField(write_only=True)
    attribute = serializers.CharField(write_only=True)
    type = serializers.CharField(read_only=True)

    class Meta:
        model = ProfileAttributeDocument
        fields = [
            'pk',
            'status',
            'downloadedAt',
            'file',
            'attribute',
            'type'
        ]

    def validate(self, data):
        """
            Serializer level verification of data.
            Verifies the received data.
        """
        data = super().validate(data)
        attribute = Attribute.objects.get(name=data['attribute'])
        if attribute.maxSize and data['file'].size > attribute.maxSize:
            raise ValidationError({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid file size",
                "details":[
                    {
                        "field": "value",
                        "error": "The file size must be bellow %s byte(s)." % (attribute.maxSize),
                        "attribute": attribute.name,
                    }
                ]
            })
        return data
    