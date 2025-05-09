from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from ..utils import valid_response, get_authenticated_partner
from ..serializers import WebhookSerializer
from ..permissions import ConfigureOnlyIfPartner
from ..models import Webhook

class WebhookViewSet(ModelViewSet):
    serializer_class = WebhookSerializer
    permission_classes = [IsAuthenticated, ConfigureOnlyIfPartner]
    queryset = Webhook.objects.all()

    @action(detail=False, methods=['post'], url_path='configure')
    def config(self, request, *args, **kwargs):
        partner = get_authenticated_partner(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(partner=partner)

        return valid_response({
                'message': "Votre url a bien été configurée.",
            })
    
    
    