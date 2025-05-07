from django.urls import path, include
from .views import ObtainPairToken, RefreshToken, Metadata,ProfileViewSet, DocumentViewSet

from rest_framework_nested import routers

profile_domain_router = routers.SimpleRouter()
profile_domain_router.register(r'profiles', ProfileViewSet, basename='profiles')
profile_router = routers.NestedSimpleRouter(profile_domain_router, r'profiles', lookup='profiles')
profile_router.register(r'documents', DocumentViewSet, basename='profiles-documents')

document_domain_router = routers.SimpleRouter()
document_domain_router.register(r'documents', DocumentViewSet, basename='documents')

urlpatterns = [
    path('auth/token/', ObtainPairToken.as_view(), name='token'),
    path('auth/token/refresh/', RefreshToken.as_view(), name='token_refresh'),
    path('metadata/', Metadata.as_view(), name='metadata'),
    path(r'', include(profile_domain_router.urls)),
    path(r'', include(profile_router.urls)),
    path(r'', include(document_domain_router.urls))
]
