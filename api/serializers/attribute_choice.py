from rest_framework import serializers

class AttributeChoiceSerializer(serializers.Serializer):
    """
        Serializer to transform Json to an AtributeChoice object
    """
    displayedName = serializers.CharField(read_only=True)
