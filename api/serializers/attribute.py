from ..models.attribute import Attribute, AttributeChoice
from .attribute_choice import AttributeChoiceSerializer

from rest_framework import serializers


class AttributeItemSerializer(serializers.Serializer):
    """
        Serializer to transform an Attribute object to JSON.
        Used to represent an Attribute when retrieved.
    """
    name = serializers.CharField(read_only=True)
    displayedName = serializers.CharField(read_only=True)


class AttributeAttributeChoiceSerializer(serializers.Serializer):
    """
    """
    attribute = AttributeItemSerializer(read_only=True)
    attribute_choice = AttributeChoiceSerializer(read_only=True)

class AttributeSerializer(serializers.ModelSerializer):
    """
        Serializer to transform JSON to an Attribute object.
        Used to create an Attribute with the given data.
    """
    attributechoice_set = AttributeChoiceSerializer(many=True, read_only=True)
    attributeattributechoice_set = AttributeAttributeChoiceSerializer(many=True, read_only=True)
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
            'attributechoice_set',
            'regex',
            'maxLength',
            'minLength',
            'maxValue',
            'minValue',
            'maxDate',
            'minDate',
            'maxSize',
            'acceptedFormat',
            'attributeattributechoice_set'
        ]