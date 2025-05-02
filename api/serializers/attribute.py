from ..models import Attribute
from .attribute_choice import AttributeChoiceItemSerializer

from rest_framework import serializers

class AttributeSerializer(serializers.ModelSerializer):
    attributechoice_set = AttributeChoiceItemSerializer(many=True, read_only=True)
    class Meta:
        model = Attribute
        fields = [
            'name',
            'displayedName',
            'type',
            'isRequired',
            'validation',
            'sensitiveData',
            'attributechoice_set'
        ]