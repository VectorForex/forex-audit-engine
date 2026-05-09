from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import TradeViewSet, AnalyticsViewSet, PerformanceTokenViewSet, UserAccountViewSet, PortfolioViewSet

router = DefaultRouter()
router.register(r'trades', TradeViewSet, basename='trade')
router.register(r'analytics', AnalyticsViewSet, basename='analytics')
router.register(r'tokens', PerformanceTokenViewSet, basename='token')
router.register(r'accounts', UserAccountViewSet, basename='account')
router.register(r'portfolio', PortfolioViewSet, basename='portfolio')

urlpatterns = [
    path('api/', include(router.urls)),
]
