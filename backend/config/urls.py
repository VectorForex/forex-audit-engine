from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import TradeViewSet, AnalyticsViewSet

router = DefaultRouter()
router.register(r'trades', TradeViewSet, basename='trade')
router.register(r'analytics', AnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('api/', include(router.urls)),
]
