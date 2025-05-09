from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from ..utils import get_profile_or_error, get_analysis_or_error, valid_response
from ..serializers import AnalysisSerializer, AnalysisItemRetrieveSerializer
from ..permissions import BelongsToPartnerToGetPatch, IsAdminToDeletePutPatch

class AnalyseViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, BelongsToPartnerToGetPatch, IsAdminToDeletePutPatch]
    serializer_class = AnalysisSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        analysis = self.get_object()

        serializer= AnalysisItemRetrieveSerializer(instance=analysis)
        return valid_response(serializer.data)
    
    def create(self, request, profiles_pk=None, *args, **kwargs):
        profile = get_profile_or_error(profiles_pk)
        self.check_object_permissions(request, profile)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        analysis = serializer.save(profile=profile)
        return valid_response({
            'message': "Vous venez de faire une demande d\'analyse pour le profile %s" % (profiles_pk),
            'pk': analysis.id,
            'status': analysis.status   
        }, code=status.HTTP_201_CREATED)
  
    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().list(request, *args, **kwargs)
        raise PermissionDenied()
    
    
    def get_object(self):
        analysis = get_analysis_or_error(self.kwargs["pk"])
        self.check_object_permissions(self.request, get_profile_or_error(analysis.profile.id))
        return analysis