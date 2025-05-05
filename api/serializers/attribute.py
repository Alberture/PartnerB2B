from ..models import Attribute
from .attribute_choice import AttributeChoiceSerializer

from rest_framework import serializers

class AttributeItemSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)

class AttributeSerializer(serializers.ModelSerializer):
    """
        Serializer to transform an Attribute object
        to a JSON format
    """
    attributechoice_set = AttributeChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Attribute
        fields = [
            'pk',
            'name',
            'displayedName',
            'type',
            'isRequired',
            'validation',
            'sensitiveData',
            'attributechoice_set'
        ]