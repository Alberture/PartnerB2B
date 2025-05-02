from rest_framework.views import APIView

from ..models import Attribute

class Metadata(APIView):
    """
        APIView that returns metadata from attributes
    """
    def get(self, request, *args, **kwargs):
        attributes = Attribute.objects.values('category')
        
        