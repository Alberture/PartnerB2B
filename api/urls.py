from django.urls import path
from .views import ObtainPairToken, RefreshToken

urlpatterns = [
    path('auth/token/', ObtainPairToken.as_view(), name='api'),
    path('auth/token/refresh/', RefreshToken.as_view(), name='token_refresh'),
]
