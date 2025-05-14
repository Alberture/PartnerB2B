from django.urls import path, include
from .views import ObtainPairToken, RefreshToken, Metadata,ProfileViewSet, DocumentViewSet, AnalyseViewSet, WebhookViewSet

from rest_framework_nested import routers

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profiles')
router.register(r'analyses', AnalyseViewSet, basename='analysis')
router.register(r'documents', DocumentViewSet, basename='documents')
router.register(r'webhooks', WebhookViewSet, basename='webhooks')

"""
profile_router = routers.NestedDefaultRouter(router, r'profiles', lookup='profiles')
profile_router.register(r'documents', DocumentViewSet, basename='profiles-documents')
profile_router.register(r'analyses', AnalyseViewSet, basename='profiles-analysis')
"""

urlpatterns = [
    path('auth/token/', ObtainPairToken.as_view(), name='token'),
    path('auth/token/refresh/', RefreshToken.as_view(), name='token_refresh'),
    path('metadata/', Metadata.as_view(), name='metadata'),
    # YOUR PATTERNS
    path('docs/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('docs/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns += router.urls# + profile_router.urls