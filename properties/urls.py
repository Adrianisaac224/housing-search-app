from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, AmenityViewSet

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'amenities', AmenityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
