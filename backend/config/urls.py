from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import TradeViewSet, AnalyticsViewSet, PerformanceTokenViewSet

router = DefaultRouter()
router.register(r'trades', TradeViewSet, basename='trade')
router.register(r'analytics', AnalyticsViewSet, basename='analytics')
router.register(r'tokens', PerformanceTokenViewSet, basename='token')

urlpatterns = [
    path('api/', include(router.urls)),
]
