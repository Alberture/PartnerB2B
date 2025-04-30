from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from datetime import datetime

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access_token_str = serializer.validated_data['access']
        access_token = AccessToken(access_token_str)
        access_exp = datetime.fromtimestamp(access_token['exp']).isoformat()

        return Response({
            'access': access_token_str,
            'access_expires': access_exp
        })