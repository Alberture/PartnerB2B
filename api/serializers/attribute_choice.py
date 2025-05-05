from rest_framework import serializers
from ..models import AttributeChoice

class AttributeChoiceSerializer(serializers.ModelSerializer):
    """
        Serializer to transform Json to an AtributeChoice object
    """
    class Meta:
        model = AttributeChoice
        fields = ['displayedName']
