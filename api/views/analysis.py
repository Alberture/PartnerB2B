from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..utils import error_response, get_profile_or_error, get_analysis_or_error, get_authenticated_partner, valid_response
from ..serializers import AnalysisSerializer, AnalysisItemSerializer, AnalysisItemRetrieveSerializer

class AnalyseViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = AnalysisSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        analysis = get_analysis_or_error(pk)
        if not analysis:
            return error_response("Cette analyse n'existe pas.")

        partner = get_authenticated_partner(request)
        profile = get_profile_or_error(analysis.profile.id, partner)  
        if not profile:
            return error_response("Cette analyse n'existe pas.")

        serializer= AnalysisItemRetrieveSerializer(instance=analysis)
        return valid_response(serializer.data)
    
    def create(self, request, profiles_pk=None, *args, **kwargs):
        if not profiles_pk:
            return error_response("Il manque l'identifiant du profil.")
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        partner = get_authenticated_partner(request)
        profile = get_profile_or_error(profiles_pk, partner)
        if not profile:
            return error_response("Ce profile n'existe pas. Veuillez vérifier l'identifiant")
        analysis = serializer.save(profile=profile)
        return valid_response({
            'message': "Vous venez de faire une demande d\'analyse pour le profile %s" % (profiles_pk),
            'pk': analysis.id,
            'status': analysis.status   
        }, code=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        return error_response()
    
    def destroy(self, request, *args, **kwargs):
        return error_response()
    
    def update(self, request, *args, **kwargs):
        return error_response()
    
    def partial_update(self, request, *args, **kwargs):
        return error_response()