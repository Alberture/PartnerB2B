from rest_framework import serializers

class CreateProfileSerializer(serializers.Serializer):
    attributes = serializers.DictField(child=[
        serializers.CharField(),
        serializers.ListField(),
    ])
