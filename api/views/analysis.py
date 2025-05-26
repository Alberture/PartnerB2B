from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed

from ..utils import valid_response
from ..serializers import AnalysisSerializer, AnalysisItemSerializer
from ..permissions import AnalysisBelongsToPartner, RetrieveOnly, IsAdminOrPartnerActivationStatusIsSuccessOrNotAllowed
from ..models import Analysis, Profile

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
    permission_classes = [IsAuthenticated, AnalysisBelongsToPartner, RetrieveOnly, IsAdminOrPartnerActivationStatusIsSuccessOrNotAllowed]
    serializer_class = AnalysisSerializer

    @extend_schema(
        examples=[
            OpenApiExample(
            name="Exemple retrieve Analysis",
            value={
                "data": {
                    "score": None,
                    "status": "pending",
                    "details": None,
                    "version": None
                },
                "meta": {
                    "timestamp": "2025-05-20T11:57:50.502833",
                    "request_id": "c1d0cf0f-09d7-410d-9e50-3e098f94106b"
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

    def get_object(self):
        analysis = Analysis.get_analysis_or_error(self.kwargs["pk"])
        self.check_object_permissions(self.request, analysis)
        return analysis