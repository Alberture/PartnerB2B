from django.urls import path
from .views import ObtainPairToken, RefreshToken, Metadata,ProfileViewSet, DocumentView

from rest_framework import routers

profiles_router = routers.SimpleRouter()
profiles_router.register(r'profiles', ProfileViewSet, basename='profiles')

documents_router = routers.SimpleRouter()
documents_router.register(r'documents', DocumentView, basename='documents')


urlpatterns = [
    path('auth/token/', ObtainPairToken.as_view(), name='token'),
    path('auth/token/refresh/', RefreshToken.as_view(), name='token_refresh'),
    path('metadata/', Metadata.as_view(), name='metadata'),
]

urlpatterns += profiles_router.urls
urlpatterns += documents_router.urls