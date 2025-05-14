from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound, MethodNotAllowed

from ..serializers import ProfileAttributeDocumentItemSerializer, ProfileAttributeDocumentSerializer
from ..utils import valid_response
from ..models import Attribute, Profile, ProfileAttributeDocument
from ..permissions import DocumentBelongsToPartnerToRead, ProfileBelongsToPartner

from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_view

from datetime import datetime

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
    permission_classes = [IsAuthenticated, DocumentBelongsToPartnerToRead, ProfileBelongsToPartner]
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
    
    def create(self, request, profiles_pk=None, *args, **kwargs):
        raise MethodNotAllowed({
            "code": status.HTTP_403_FORBIDDEN,
            "message": "Not Allowed",
            "details":[
                {
                    "error": "You are not allowed to POST.",
                    "path": request.path
                }
            ]
        })
    
    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed({
            "code": status.HTTP_403_FORBIDDEN,
            "message": "Not Allowed",
            "details":[
                {
                    "error": "You are not allowed to GET.",
                    "path": request.path
                }
            ]
        })

    def destroy(self, request, pk, *args, **kwargs):
        raise MethodNotAllowed({
            "code": status.HTTP_403_FORBIDDEN,
            "message": "Not Allowed",
            "details":[
                {
                    "error": "You are not allowed to DELETE.",
                    "path": request.path
                }
            ]
        })
    
    def update(self, request, pk, *args, **kwargs):
        raise MethodNotAllowed({
            "code": status.HTTP_403_FORBIDDEN,
            "message": "Not Allowed",
            "details":[
                {
                    "error": "You are not allowed to PUT.",
                    "path": request.path
                }
            ]
        })
    
    def partial_update(self, request, pk, *args, **kwargs):
        raise MethodNotAllowed({
            "code": status.HTTP_403_FORBIDDEN,
            "message": "Not Allowed",
            "details":[
                {
                    "error": "You are not allowed to PATCH.",
                    "path": request.path
                }
            ]
        })
    
    def get_object(self):
        document = ProfileAttributeDocument.get_docuement_or_error(self.kwargs["pk"])
        self.check_object_permissions(self.request, document)
        return document