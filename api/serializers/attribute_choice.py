from rest_framework import serializers

class AttributeChoiceSerializer(serializers.Serializer):
    """
        Serializer to transform JSON to an AtributeChoice object.
        Used to represent an AttributeChoice when retrieved.
    """
    displayedName = serializers.CharField(read_only=True)
