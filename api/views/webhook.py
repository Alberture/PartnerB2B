from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import status

from ..utils import valid_response
from ..serializers import WebhookSerializer, WebhookItemSerializer
from ..permissions import WebhookBelongsToParnter, CantListUpdateCreate, IsAdminOrPartnerActivationStatusIsSuccessOrNotAllowed
from ..models import Webhook, Partner

from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_view

from datetime import datetime

@extend_schema_view(
    create=extend_schema(exclude=True),
    update=extend_schema(exclude=True),
    list=extend_schema(exclude=True),
)
class WebhookViewSet(ModelViewSet):
    """
        ViewSet that manages Webhooks objects.
    """
    serializer_class = WebhookSerializer
    permission_classes = [IsAuthenticated, WebhookBelongsToParnter, CantListUpdateCreate, IsAdminOrPartnerActivationStatusIsSuccessOrNotAllowed]
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
                "data": {
                    "message": "Votre url a bien été configurée."
                },
                "meta": {
                    "timestamp": "2025-05-13T21:50:38.073740",
                    "request_id": "f547e99b-b05e-4913-b0ee-5d3c5492b352"
                }
            },
            response_only=True
            )
        ]
    )
    @action(detail=False, methods=['post'], url_path='configure')
    def config(self, request, *args, **kwargs):
        partner = Partner.get_authenticated_partner(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(partner=partner)

        return valid_response({
                'message': "Votre url a bien été configurée.",
            }, request.id)

    @extend_schema(
        examples=[
            OpenApiExample(
            name="Example delete Webhook",
            value={
                "data": {
                    "message": "Votre webhook a bien été supprimé."
                },
                "meta": {
                    "timestamp": "2025-05-14T07:31:59.463958",
                    "request_id": "cd21c104-756b-44a2-b5f0-f25bccd7cb0a"
                }
            },
            response_only=True
            )
        ],
        responses=200
    )
    def destroy(self, request, pk, *args, **kwargs):
        super().destroy(request, pk, *args, **kwargs)
        return valid_response({
            "message": "Votre webhook a bien été supprimé."
        }, request.id)
    
    @extend_schema(
        request=WebhookSerializer,
        examples=[
            OpenApiExample(
            name="Example request body for PATCH Webhook",
            value={
                'url': 'https://localhost/webhook/',
            },
            request_only=True
            ),
            OpenApiExample(
            name="Exemple PATCH Webhook",
            value={
                "data": {
                    'message': "Votre url a bien été modifée."
                },
                "meta": {
                    "timestamp": "2025-05-13T21:50:38.073740",
                    "request_id": "f547e99b-b05e-4913-b0ee-5d3c5492b352"
                }
            },
            response_only=True
            )
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        partner = Partner.get_authenticated_partner(request)
        serializer = self.serializer_class(data=request.data, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save(partner=partner)

        return valid_response({
                'message': "Votre url a bien été modifée.",
            }, request.id)
    
    def get_object(self):
        webhook = Webhook.get_webhook_or_error(self.kwargs["pk"])
        self.check_object_permissions(self.request, webhook)

        return webhook
    
    @extend_schema(
        examples=[
            OpenApiExample(
            name="Exemple retrieve Webhook",
            value={
                "data": {
                    "url": "url"
                },
                "meta": {
                    "timestamp": "2025-05-14T08:08:41.902521",
                    "request_id": "c02218c5-bb9c-4ef9-9b99-e821bf62be79"
                }
            },
            response_only=True
            )
        ]
    )
    def retrieve(self, request, pk, *args, **kwargs):
        webhook = self.get_object()
        serializer = WebhookItemSerializer(webhook)
        return valid_response(serializer.data, request.id)
    
    