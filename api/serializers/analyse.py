from rest_framework import serializers

class AnalyseItemSerializer(serializers.Serializer):
    """
        Serializer to transform Analyse object to JSON format
    """
    score = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    details = serializers.CharField(read_only=True)
    version = serializers.CharField(read_only=True)
