from rest_framework import serializers

from ..models import Analysis

class AnalysisItemRetrieveSerializer(serializers.Serializer):
    score = serializers.IntegerField(read_only=True)
    details = serializers.CharField(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)
    completedAt = serializers.DateTimeField(read_only=True)

class AnalysisItemSerializer(serializers.Serializer):
    """
        Serializer to transform Analysis object to JSON format
    """
    score = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    details = serializers.CharField(read_only=True)
    version = serializers.CharField(read_only=True)

class AnalysisSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    class Meta:
        model = Analysis
        fields = [
            'pk',
            'status',
        ]