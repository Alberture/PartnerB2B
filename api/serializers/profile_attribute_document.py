from rest_framework import serializers

from ..models import ProfileAttributeDocument

class ProfileAttributeDocumentItemSerializer(serializers.ModelSerializer):
    """
        Serializer to transform Document object to JSON format
    """
    #profile = ProfileItemSerializer(read_only=True)
    title = serializers.CharField(read_only=True)
    file = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)
    downloadedAt = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    metadata = serializers.CharField(read_only=True)
    class Meta:
        model = ProfileAttributeDocument
        fields = [
            'profile',
            'title',
            'file',
            'type',
            'downloadedAt',
            'status',
            'metadata',
        ]

class ProfileAttributeDocumentSerializer(serializers.ModelSerializer):
   
    pk = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    downloadedAt = serializers.DateTimeField(read_only=True)
    file = serializers.ImageField(write_only=True)

    class Meta:
        model = ProfileAttributeDocument
        fields = [
            'pk',
            'status',
            'downloadedAt',
            'type',
            'file'
        ]
