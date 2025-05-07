from django.db.models import Count

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..serializers import ProfileAttributeDocumentItemSerializer
from ..utils import get_docuement_or_error, error_response

class DocumentView(ModelViewSet):
    """
        APIView with only a get method that lists
        all attributes in each category of attributes
        and their specificities
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileAttributeDocumentItemSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        docuement = get_docuement_or_error(pk)
        if not docuement:
            error_response("Ce document n'existe pas.")
        serializer= self.serializer_class(instance=docuement)
        return Response(serializer.data)

        