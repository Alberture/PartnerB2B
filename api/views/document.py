from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound

from ..serializers import ProfileAttributeDocumentItemSerializer, ProfileAttributeDocumentSerializer
from ..utils import valid_response
from ..models import Attribute, Profile, ProfileAttributeDocument
from ..permissions import DocumentBelongsToPartnerToRead, IsAdminToDeletePutPatch, ProfileBelongsToPartner

from drf_spectacular.utils import extend_schema, OpenApiExample

from datetime import datetime

class DocumentViewSet(ModelViewSet):
    """
        ViewSet that manages ProfileAttributeDocument objects.
    """
    permission_classes = [IsAuthenticated, DocumentBelongsToPartnerToRead, IsAdminToDeletePutPatch, ProfileBelongsToPartner]
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
    
    @extend_schema(
        request=ProfileAttributeDocumentSerializer,
        examples=[
            OpenApiExample(
            name="Exemple create Document",
            value={
                "data": {
                    "pk": 13,
                    "status": "pending",
                    "downloadedAt": "2025-05-12T12:10:37.486892Z",
                    "type": "png"
                },
                "meta": {
                    "timestamp": "2025-05-12T12:10:37.538076"
                }
            },
            response_only=True
            )
        ],
        responses=ProfileAttributeDocumentSerializer
    )
    def create(self, request, profiles_pk=None, *args, **kwargs):
        profile = Profile.get_profile_or_error(profiles_pk)
        self.check_object_permissions(request, profile)
        serializer = ProfileAttributeDocumentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            document_attribute = Attribute.get_attribute_or_error(request.data['attribute'])
            if document_attribute.category != 'documents':
                document_attributes = Attribute.objects.filter(category="documents")
                raise ValidationError({
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Erreur de validation",
                    "details":[
                        { 
                            "field": "attribute",
                            "error": "L'attribute selectionnée doit faire parti de la famille des documents. Liste des attributs dans cette catégorie : %s" % (list(map(str,document_attributes)))
                        }
                    ]
                })
            type=str(request.data['file'])[str(request.data['file']).find(".")+1:]
            serializer.save(attribute=document_attribute, profile=profile, type=type)
            return valid_response(serializer.data, request.id, status.HTTP_201_CREATED)

    @extend_schema(exclude=True)
    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().list(request, *args, **kwargs)
        raise PermissionDenied({
            "code": status.HTTP_403_FORBIDDEN,
            "message": "Permission Denied",
            "details": [
                {"error": "You must be an admin to perform this action."}
            ]
        })

    @extend_schema(exclude=True)
    def destroy(self, request, pk, *args, **kwargs):
        return super().destroy(request, pk, *args, **kwargs)
    
    @extend_schema(exclude=True)
    def update(self, request, pk, *args, **kwargs):
        return super().update(request, pk, *args, **kwargs)
    
    @extend_schema(exclude=True)
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)
    
    def get_object(self):
        document = ProfileAttributeDocument.get_docuement_or_error(self.kwargs["pk"])
        self.check_object_permissions(self.request, document)
        return document
