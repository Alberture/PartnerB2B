from django.db.models import Count

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError

from ..serializers import ProfileAttributeDocumentItemSerializer, ProfileAttributeDocumentSerializer
from ..utils import get_docuement_or_error, error_response, get_profile_or_error, get_authenticated_partner, get_attribute_or_error, valid_response
from ..models import Attribute
from ..permissions import BelongsToPartnerToGetPatch

class DocumentViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, BelongsToPartnerToGetPatch]
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
        return error_response(
            message="Erreur de permission", 
            code=status.HTTP_403_FORBIDDEN,
            details=[
                {"error": "Vous n'êtes pas autrorisé à réaliser cette action."}
            ]
        )
    
    def get_object(self):
        analysis = get_docuement_or_error(self.kwargs["pk"])
        self.check_object_permissions(self.request, get_profile_or_error(analysis.profile.id))
        return analysis
