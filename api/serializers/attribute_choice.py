from rest_framework import serializers
from ..models import AttributeChoice

class AttributeChoiceSerializer(serializers.ModelSerializer):
    """
        Serializer to transform an AttributeChoice object 
        to a JSON format
    """

    class Meta:
        model = AttributeChoice
        fields = ['displayedName']
