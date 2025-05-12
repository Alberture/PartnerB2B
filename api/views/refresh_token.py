from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime

from ..utils import valid_response

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, inline_serializer, extend_schema_serializer
from drf_spectacular.types import OpenApiTypes

class RefreshToken(TokenRefreshView):
    """
        Class that inherit from TokenRefreshView (used to 
        generate refresh tokens) to custom the returned 
        Response when refreshing an access token
    """
    serializer_class = TokenRefreshSerializer

    @extend_schema(
        examples=[
            OpenApiExample('Example', value={'user': 123}, request_only=True)
        ]
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
            })