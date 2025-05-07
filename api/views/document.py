from django.db.models import Count

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..serializers import ProfileAttributeDocumentItemSerializer, ProfileAttributeDocumentSerializer
from ..utils import get_docuement_or_error, error_response, get_profile_or_error, get_authenticated_partner, get_attribute_or_error, valid_response
from ..models import Attribute

class DocumentViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileAttributeDocumentItemSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        docuement = get_docuement_or_error(pk)
        if not docuement:
            error_response("Ce document n'existe pas.")

        partner = get_authenticated_partner(request)
        profile = get_profile_or_error(docuement.profile.id, partner)  
        if not profile:
            return error_response("Ce document n'existe pas.")

        serializer= self.serializer_class(instance=docuement)
        return valid_response(serializer.data)
    
    def create(self, request, profiles_pk=None, *args, **kwargs):
        if not profiles_pk:
            return error_response("Il manque l'identifiant du profil.")
        
        serializer = ProfileAttributeDocumentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            document_attribute = get_attribute_or_error(request.data['attribute'])
            if not document_attribute:
                error_response("Ce attribute n'existe pas")
            if document_attribute.documents != 'documents':
                return error_response("Cet attribute ne correspond pas à un doccuemnt")
            partner = get_authenticated_partner(request)
            profile = get_profile_or_error(profiles_pk, partner)
            if not profile:
                return error_response("Ce profile n'existe pas. Veuillez vérifier l'identifiant")

            serializer.save(attribute=document_attribute, profile=profile)
            return valid_response(serializer.data, status.HTTP_201_CREATED)

        error_response("Le format des données n'est pas respecté")

    def destroy(self, request, pk, *args, **kwargs):
        if request.user.is_staff:
            return super().destroy(request, pk, *args, **kwargs)
        return error_response("Vous n'êtes pas autrorisé à réaliser cette action.", code=status.HTTP_403_FORBIDDEN)
    
    def update(self, request, pk, *args, **kwargs):
        if request.user.is_staff:
            return super().update(request, pk, *args, **kwargs)
        return error_response("Vous n'êtes pas autrorisé à réaliser cette action.", code=status.HTTP_403_FORBIDDEN)

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().list(request, *args, **kwargs)
        return error_response("Vous n'êtes pas autrorisé à réaliser cette action.", code=status.HTTP_403_FORBIDDEN)
    
    def partial_update(self, request, pk, *args, **kwargs):
        if request.user.is_staff:
            return super().partial_update(request, pk, *args, **kwargs)
        return error_response("Vous n'êtes pas autrorisé à réaliser cette action.", code=status.HTTP_403_FORBIDDEN)

        