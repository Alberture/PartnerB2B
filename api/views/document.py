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
                        "pk": 439,
                        "createdAt": "2025-05-20T08:33:07.727323Z",
                        "updatedAt": "2025-05-20T08:33:07.727369Z",
                        "status": "draft",
                        "externalReference": "reference"
                    },
                    "file": "documents/document_4IhNFgL_Fgm2F4j.pdf",
                    "type": "pdf",
                    "downloadedAt": "2025-05-20T11:55:58.957300Z",
                    "status": "pending",
                    "metadata": None
                },
                "meta": {
                    "timestamp": "2025-05-20T11:58:24.436578",
                    "request_id": "7343247c-6654-4be2-952f-0ab98048e769"
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