from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import serializers
from datetime import datetime

from ..utils import valid_response

from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer

class RefreshToken(TokenRefreshView):
    """
        Class that inherit from TokenRefreshView (used to 
        generate refresh tokens) to custom the returned 
        Response when refreshing an access token
    """
    serializer_class = TokenRefreshSerializer

    @extend_schema(
        request=inline_serializer("ObtainPairTokenSerializer", fields={
            'apiKey': serializers.CharField()
        }),
        examples=[
            OpenApiExample(
            name="Example request body for refresh token",
            value={
                'refresh': 'YOUR_REFRESH_TOKEN',
            },
            request_only=True
            ),
            OpenApiExample(
            name="Exemple refresh token",
            value={
                "data": {
                    "access": "YOUR_NEW_ACCESS_TOKEN",
                    "access_expires": "2025-05-13T10:42:53"
                },
                "meta": {
                    "timestamp": "2025-05-12T10:42:54.520677"
                }
            },
            response_only=True
            )
        ],
        responses=TokenRefreshSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        access_token_str = serializer.validated_data['access']
        access_token = AccessToken(access_token_str)
        access_exp = datetime.fromtimestamp(access_token['exp']).isoformat()

        return valid_response({
                'access': access_token_str,
                'access_expires': access_exp
            }, request.id)