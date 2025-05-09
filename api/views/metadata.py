from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models import Attribute
from ..serializers import AttributeSerializer
from ..utils import valid_response

class Metadata(APIView):
    """
        APIView with only a get method that lists
        all attributes in each category of attributes
        and their specificities
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        categories = Attribute.objects.values('category').distinct()
        result = {}
        for categorie in categories:
            attributes = Attribute.objects.filter(category=categorie['category'])
            serializer = AttributeSerializer(attributes, many=True)
            result[categorie['category']] = serializer.data
        
        return valid_response(result)

        