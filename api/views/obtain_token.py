from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.views import APIView
from datetime import datetime

from ..models import Partner

class ObtainPairToken(APIView):
    """
        APIView to obtain refresh and access token 
        for a partner with a valid APIKey
    """

    def post(self, request, *args, **kwargs):
        try:
            partner = Partner.objects.get(apiKey=request.data['apiKey'])
        except:
            return Response({'error': 'API key was not found'})
        
        class PartnerUserWrapper:
            """
                Since I'm using django JWT I need to pass an User-like object to the RefreshToken object
                because the RefreshToken object is based on the User object
            """
            def __init__(self, id): self.id = id
            @property
            def is_active(self): return True  # required by JWT

        partner_user = PartnerUserWrapper(partner.id)

        refresh_token = RefreshToken.for_user(partner_user)
        refresh_expire = datetime.fromtimestamp(refresh_token['exp']).isoformat()
        
        access_token = refresh_token.access_token
        access_expire = datetime.fromtimestamp(access_token['exp']).isoformat()

        return Response({
            "access": str(access_token),
            "refresh": str(refresh_token),
            "access_expire": access_expire,
            "refesh_expire": refresh_expire,
        })    