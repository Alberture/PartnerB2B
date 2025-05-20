from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed

from ..serializers import ProfileAttributeDocumentItemSerializer
from ..utils import valid_response
from ..models import ProfileAttributeDocument
from ..permissions import DocumentBelongsToPartnerToRead, RetrieveOnly, IsAdminOrPartnerActivationStatusIsSuccessOrNotAllowed

from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_view

@extend_schema_view(
    create=extend_schema(exclude=True),
    list=extend_schema(exclude=True),
    update=extend_schema(exclude=True),
    destroy=extend_schema(exclude=True),
    partial_update=extend_schema(exclude=True),
)
class DocumentViewSet(ModelViewSet):
    """
        ViewSet that manages ProfileAttributeDocument objects.
    """
    permission_classes = [
        IsAuthenticated, 
        DocumentBelongsToPartnerToRead,
        RetrieveOnly,
        IsAdminOrPartnerActivationStatusIsSuccessOrNotAllowed
    ]
    serializer_class = ProfileAttributeDocumentItemSerializer

    @extend_schema(
        examples=[
            OpenApiExample(
            name="Exemple retrieve Document",
            value={
                "data": {
                    "profile": {
                        "pk": 297,
                        "createdAt": "2025-05-09T12:14:27.693624Z",
                        "updatedAt": "2025-05-12T09:56:39.629783Z",
                        "status": "complete",
                        "externalReference": ""
                    },
                    "title": "",
                    "file": "documents/test.png",
                    "type": "png",
                    "downloadedAt": "2025-05-09T12:16:06.840877Z",
                    "status": "pending",
                    "metadata": None
                },
                "meta": {
                    "timestamp": "2025-05-12T12:05:48.747117"
                }
            },
            response_only=True
            )
        ],
        responses=ProfileAttributeDocumentItemSerializer
    )
    def retrieve(self, request, pk, *args, **kwargs):
        docuement = self.get_object()  
        serializer= self.serializer_class(instance=docuement)
        return valid_response(serializer.data, request.id)
    
    def get_object(self):
        document = ProfileAttributeDocument.get_docuement_or_error(self.kwargs["pk"])
        self.check_object_permissions(self.request, document)
        return document