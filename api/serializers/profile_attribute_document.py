from rest_framework import serializers

from ..models import ProfileAttributeDocument

class ProfileAttributeDocumentItemSerializer(serializers.Serializer):
    """
        Serializer to transform Document object to JSON format
    """
    file = serializers.CharField(read_only=True)
    titre = serializers.CharField(read_only=True)

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
