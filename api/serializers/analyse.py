from rest_framework import serializers
from ..models import Analyse

class AnalyseItemSerializer(serializers.Serializer):
    score = serializers.IntegerField(read_only=True)