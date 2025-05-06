from rest_framework import serializers

class ProfileAttributeDocumentItemSerializer(serializers.Serializer):
    """
        Serializer to transform Document object to JSON format
    """
    file = serializers.CharField(read_only=True)
    titre = serializers.CharField(read_only=True)
