from rest_framework import serializers

class DocumentItemSerializer(serializers.Serializer):
    file = serializers.CharField(read_only=True)
