from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed

from ..utils import valid_response
from ..serializers import AnalysisSerializer, AnalysisItemSerializer
from ..permissions import AnalysisBelongsToPartner, IsAdminOrHasEnoughTries, ProfileBelongsToPartner
from ..models import Profile, Analysis, Partner

from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_view

@extend_schema_view(
    create=extend_schema(exclude=True),
    list=extend_schema(exclude=True),
    update=extend_schema(exclude=True),
    destroy=extend_schema(exclude=True),
    partial_update=extend_schema(exclude=True),
)
class AnalyseViewSet(ModelViewSet):
    """
        ViewSet that manages Analysis objects.
    """
    permission_classes = [IsAuthenticated, AnalysisBelongsToPartner, IsAdminOrHasEnoughTries, ProfileBelongsToPartner]
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
        responses=AnalysisItemSerializer,
    )
    def retrieve(self, request, pk, *args, **kwargs):
        analysis = self.get_object()

        serializer= AnalysisItemSerializer(instance=analysis)
        return valid_response(serializer.data, request.id)

    def create(self, request, profiles_pk, *args, **kwargs):
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
        """
        analysis = self.get_object()
        serializer = self.serializer_class(data=request.data, instance=analysis)
        serializer.is_valid(raise_exception=True)
        analysis = serializer.save(profile=analysis.profile)
        partner = Partner.get_authenticated_partner(request)
        if partner.limitUsage:
            partner.limitUsage -= 1
            partner.save()
        
        return valid_response({
            'message': "Vous venez de faire une nouvelle demande d\'analyse pour le profile %s" % (profiles_pk),
            'status': analysis.status   
        }, request.id)
        """
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
        analysis = Analysis.get_analysis_or_error(self.kwargs["pk"])
        self.check_object_permissions(self.request, analysis)
        return analysis