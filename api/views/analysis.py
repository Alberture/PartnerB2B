from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from ..utils import get_profile_or_error, get_analysis_or_error, valid_response
from ..serializers import AnalysisSerializer, AnalysisItemSerializer
from ..permissions import AnalysisBelongsToPartnerToRead, IsAdminToDeletePutPatch

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, inline_serializer
from drf_spectacular.types import OpenApiTypes

from datetime import datetime

class AnalyseViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, AnalysisBelongsToPartnerToRead, IsAdminToDeletePutPatch]
    serializer_class = AnalysisSerializer
    

    @extend_schema(
        examples=[
            OpenApiExample(
            name="Exemple retrieve Analysis",
            value={
                "data": {
                    "score": None,
                    "details": None,
                    "createdAt": "2025-05-09T12:16:43.114001Z",
                    "completedAt": None
                },
                "meta": {
                    "timestamp": "2025-05-12T12:02:34.778803"
                }
            },
            response_only=True
            )
        ],
        responses=AnalysisItemSerializer
    )
    def retrieve(self, request, pk, *args, **kwargs):
        analysis = self.get_object()

        serializer= AnalysisItemSerializer(instance=analysis)
        return valid_response(serializer.data)
    
    @extend_schema(
        examples=[
            OpenApiExample(
            name="Exemple create Analysis",
            value={
                "data": {
                    "message": "Vous venez de faire une demande d'analyse pour le profile 297",
                    "pk": 13,
                    "status": "pending"
                },
                "meta": {
                    "timestamp": "2025-05-12T12:04:24.219023"
                }
            },
            response_only=True
            )
        ],
        responses=AnalysisSerializer
    )
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
    
    @extend_schema(exclude=True)
    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().list(request, *args, **kwargs)
        raise PermissionDenied()
    
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
        analysis = get_analysis_or_error(self.kwargs["pk"])
        self.check_object_permissions(self.request, analysis)
        return analysis