from django.urls import path
from .views import ObtainPairToken, RefreshToken, Metadata

urlpatterns = [
    path('auth/token/', ObtainPairToken.as_view(), name='token'),
    path('auth/token/refresh/', RefreshToken.as_view(), name='token_refresh'),
    path('metadata/', Metadata.as_view(), name='metadata')
]
