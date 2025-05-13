from django.urls import path, include
from .views import ObtainPairToken, RefreshToken, Metadata,ProfileViewSet, DocumentViewSet, AnalyseViewSet, WebhookViewSet

from rest_framework_nested import routers

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

profile_domain_router = routers.SimpleRouter()
profile_domain_router.register(r'profiles', ProfileViewSet, basename='profiles')
profile_router = routers.NestedSimpleRouter(profile_domain_router, r'profiles', lookup='profiles')
profile_router.register(r'documents', DocumentViewSet, basename='profiles-documents')
profile_router.register(r'analyses', AnalyseViewSet, basename='profiles-analysis')

document_domain_router = routers.SimpleRouter()
document_domain_router.register(r'documents', DocumentViewSet, basename='documents')

analysis_domain_router = routers.SimpleRouter()
analysis_domain_router.register(r'analyses', AnalyseViewSet, basename='analysis')

webhook_domain_router = routers.SimpleRouter()
webhook_domain_router.register(r'webhooks', WebhookViewSet, basename='webhooks')

urlpatterns = [
    path('auth/token/', ObtainPairToken.as_view(), name='token'),
    path('auth/token/refresh/', RefreshToken.as_view(), name='token_refresh'),
    path('metadata/', Metadata.as_view(), name='metadata'),
    path(r'', include(profile_domain_router.urls)),
    path(r'', include(profile_router.urls)),
    path(r'', include(document_domain_router.urls)),
    path(r'', include(analysis_domain_router.urls)),
    path(r'', include(webhook_domain_router.urls)),   
    # YOUR PATTERNS
    path('docs/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('docs/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
