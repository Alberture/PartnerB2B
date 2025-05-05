from rest_framework import serializers

class AnalyseItemSerializer(serializers.Serializer):
    score = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    details = serializers.CharField(read_only=True)
    version = serializers.CharField(read_only=True)
