from rest_framework import serializers

from ..models.profile_attribute_document import ProfileAttributeDocument

class ProfileDocumentSerializer(serializers.Serializer):
    """
        Serializer to transform a Profile object to JSON.
        Mainly to avoid infinite include.
    """
    pk = serializers.IntegerField(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    externalReference = serializers.CharField(read_only=True)

class ProfileAttributeDocumentItemSerializer(serializers.ModelSerializer):
    """
        Serializer to transform a ProfileAttributeDocument object to JSON format.
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
    """
    pk = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    downloadedAt = serializers.DateTimeField(read_only=True)
    file = serializers.ImageField(write_only=True)
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

    