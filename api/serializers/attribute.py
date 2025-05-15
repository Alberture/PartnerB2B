from ..models.attribute import Attribute, AttributeChoice
from .attribute_choice import AttributeChoiceSerializer

from rest_framework import serializers

class AttributeItemSerializer(serializers.Serializer):
    """
        Serializer to transform an Attribute object to JSON.
    """
    name = serializers.CharField(read_only=True)

class AttributeSerializer(serializers.ModelSerializer):
    """
        Serializer to transform JSON to an Attribute object.
    """
    choices = serializers.SerializerMethodField()
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
            'choices'
        ]

    def get_choices(self, attribute):
        qs = attribute.choices.filter(attributeattributechoice__is_choice=True)
        serializer = AttributeChoiceSerializer(instance=qs, many=True)
        return serializer.data