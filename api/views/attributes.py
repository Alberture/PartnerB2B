from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from ..models import Attribute
from ..serializers import AttributeSerializer

class Metadata(APIView):
    """
        APIView that returns metadata from attributes
    """
    def get(self, request, *args, **kwargs):
        categories = Attribute.objects.values('category').distinct()
        result = {}
        for categorie in categories:
            attributes = Attribute.objects.filter(category=categorie['category'])
            serializer = AttributeSerializer(attributes, many=True)
            result[categorie['category']] = serializer.data
        
        return Response(result)

        