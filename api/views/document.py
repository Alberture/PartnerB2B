from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from ..serializers import ProfileAttributeDocumentItemSerializer, ProfileAttributeDocumentSerializer
from ..utils import get_docuement_or_error, get_profile_or_error, get_attribute_or_error, valid_response
from ..models import Attribute
from ..permissions import DocumentBelongsToPartnerToGetPatch, IsAdminToDeletePutPatch

class DocumentViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, DocumentBelongsToPartnerToGetPatch, IsAdminToDeletePutPatch]
    serializer_class = ProfileAttributeDocumentItemSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        docuement = self.get_object()  

        serializer= self.serializer_class(instance=docuement)
        return valid_response(serializer.data)
    
    def create(self, request, profiles_pk=None, *args, **kwargs):
        profile = get_profile_or_error(profiles_pk)
        self.check_object_permissions(request, profile)
        serializer = ProfileAttributeDocumentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            document_attribute = get_attribute_or_error(request.data['attribute'])
            if document_attribute.category != 'documents':
                document_attributes = Attribute.objects.filter(category="documents")
                raise ValidationError({
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Erreur de validation",
                    "details":[
                        { 
                            "field": "attribute",
                            "error": "L'attribute selectionnée doit faire parti de la famille des documents. Liste des attributs dans cette catégorie : %s" % (list(document_attributes))
                        }
                    ]
                })
            serializer.save(attribute=document_attribute, profile=profile)
            return valid_response(serializer.data, status.HTTP_201_CREATED)
        
    
    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().list(request, *args, **kwargs)
        raise PermissionDenied()
    
    def get_object(self):
        document = get_docuement_or_error(self.kwargs["pk"])
        self.check_object_permissions(self.request, document)
        return document
