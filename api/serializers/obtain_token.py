from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from ..models import Partner

class ObtainTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
    
    