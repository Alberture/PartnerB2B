
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import serializers
from datetime import datetime

from django.contrib.auth.models import User

from ..utils import valid_response
from ..models import Partner

from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer, OpenApiResponse

from ..serializers import ProfileSerializer

class ObtainPairToken(APIView):
    """
        APIView to obtain refresh and access token for a partner with a valid APIKey.
    """
    @extend_schema(
        request=inline_serializer(
            name="ObtainPairTokenSerializer",
            fields={
                'apiKey': serializers.CharField()
            }
        ),
        responses=OpenApiResponse(
            response=inline_serializer(
                name="ObtainPairTokenResponse",
                fields={
                    "data": serializers.DictField(
                        child=serializers.CharField()
                    ),
                    "meta": serializers.DictField(
                        child=serializers.CharField()
                    )
                }
            ),
            examples=[
                OpenApiExample(
                    name="Exemple obtain token",
                    value={
                        "data": {
                            "access": "YOUR_ACCESS_TOKEN",
                            "refresh": "YOUR_REFRESH_TOKEN",
                            "access_expire": "2025-05-13T09:12:06",
                            "refesh_expire": "2025-05-19T09:12:06"
                        },
                        "meta": {
                            "timestamp": "2025-05-12T09:12:06.926977"
                        }
                    },
                    response_only=True
                )
            ]
        ),
        examples=[
            OpenApiExample(
                name="Example request body for obtain token",
                value={"apiKey": "YOUR_API_KEY"},
                request_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        partner = Partner.get_partner_or_error(request.data.get('apiKey'))
        class PartnerUserWrapper:
            """
                Since I'm using django JWT I need to pass an User-like object to the RefreshToken object
                because the RefreshToken object is based on the User object
            """
            def __init__(self, id): 
                self.id = id
                try:
                    partner = Partner.objects.get(pk=id)
                except Partner.DoesNotExist:
                    user = User.objects.create_user(username=partner.name)

            @property
            def is_active(self): return True  # required by JWT

        partner_user = PartnerUserWrapper(partner.id)
        refresh_token = RefreshToken.for_user(partner_user)
        refresh_expire = datetime.fromtimestamp(refresh_token['exp']).isoformat()
        
        access_token = refresh_token.access_token
        access_expire = datetime.fromtimestamp(access_token['exp']).isoformat()

        return valid_response({
                "access": str(access_token),
                "refresh": str(refresh_token),
                "access_expire": access_expire,
                "refesh_expire": refresh_expire,
            }, request.id)