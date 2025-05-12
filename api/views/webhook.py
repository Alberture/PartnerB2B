from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from ..utils import valid_response, get_authenticated_partner
from ..serializers import WebhookSerializer
from ..permissions import ConfigureOnlyIfPartner
from ..models import Webhook

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, inline_serializer
from drf_spectacular.types import OpenApiTypes

from datetime import datetime

@extend_schema()
class WebhookViewSet(ModelViewSet):
    serializer_class = WebhookSerializer
    permission_classes = [IsAuthenticated, ConfigureOnlyIfPartner]
    queryset = Webhook.objects.all()

    @extend_schema(
        request=WebhookSerializer,
        examples=[
            OpenApiExample(
            name="Example request body for config Webhook",
            value={
                'url': 'https://localhost/webhook/',
            },
            request_only=True
            ),
            OpenApiExample(
            name="Exemple config Webhook",
            value={
                "pk": 0,
                "url": "https://localhost/webhook/"
            },
            response_only=True
            )
        ]
    )
    @action(detail=False, methods=['post'], url_path='configure')
    def config(self, request, *args, **kwargs):
        partner = get_authenticated_partner(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(partner=partner)

        return valid_response({
                'message': "Votre url a bien été configurée.",
            })
    
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
    
    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(exclude=True)
    def retrieve(self, request, pk, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)
    
    