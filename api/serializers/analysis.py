from rest_framework import serializers

from ..models.analysis import Analysis

class AnalysisItemSerializer(serializers.Serializer):
    """
        Serializer to transform an Analysis object to JSON.
        Used to represent an Analysis when retrieved.
    """
    score = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    details = serializers.CharField(read_only=True)
    version = serializers.CharField(read_only=True)

class AnalysisSerializer(serializers.ModelSerializer):
    """
        Serializer to transform JSON to an Analysis object.
        Used to create Analysis with the given data.
    """
    pk = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    class Meta:
        model = Analysis
        fields = [
            'pk',
            'status',
        ]