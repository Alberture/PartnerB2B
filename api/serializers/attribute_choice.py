from rest_framework import serializers

class AttributeChoiceItemSerializer(serializers.Serializer):
    displayedName = serializers.CharField(read_only=True)
