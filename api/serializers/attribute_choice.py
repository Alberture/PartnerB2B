from rest_framework import serializers
from ..models import AttributeChoice

class AttributeChoiceSerializer(serializers.Serializer):
    """
        Serializer to transform Json to an AtributeChoice object
    """
    displayedName = serializers.CharField(read_only=True)
