from django.db.models import Count

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..serializers import ProfileAttributeDocumentItemSerializer, ProfileAttributeDocumentSerializer
from ..utils import get_docuement_or_error, error_response, get_profile_or_error, get_authenticated_partner
from ..models import Attribute

class DocumentViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileAttributeDocumentItemSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        docuement = get_docuement_or_error(pk)
        if not docuement:
            error_response("Ce document n'existe pas.")
        serializer= self.serializer_class(instance=docuement)
        return Response(serializer.data)
    
    def create(self, request, profiles_pk=None, *args, **kwargs):
        if not profiles_pk:
            return error_response("Il manque l'identifiant du profil.")
        
        serializer = ProfileAttributeDocumentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            document_attribute = Attribute.objects.get(name="document")
            partner = get_authenticated_partner(request)
            profile = get_profile_or_error(profiles_pk, partner)
            if not profile:
                return error_response("Ce profile n'existe pas. Veuillez vérifier l'identifiant")

            serializer.save(attribute=document_attribute, profile=profile)
            return Response(serializer.data)

        error_response("Le format des données n'est pas respecté")

    def list(self, request, *args, **kwargs):
        return error_response()
    
    def destroy(self, request, *args, **kwargs):
        return error_response()
    
    def update(self, request, *args, **kwargs):
        return error_response()
    
    def partial_update(self, request, *args, **kwargs):
        return error_response()

        