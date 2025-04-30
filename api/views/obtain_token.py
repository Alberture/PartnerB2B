from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from datetime import datetime

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access_token = AccessToken(serializer.validated_data['access'])
        refresh_token = RefreshToken(serializer.validated_data['refresh'])
        access_exp = datetime.fromtimestamp(access_token['exp']).isoformat()
        refresh_exp = datetime.fromtimestamp(refresh_token['exp']).isoformat()
        
        return Response({
            'access': str(access_token),
            'refresh': str(refresh_token),
            'access_expires': access_exp,
            'refresh_expires': refresh_exp,
        })