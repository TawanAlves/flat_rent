from django.urls import path, include
from core.views import FlatViewSet
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'flats', FlatViewSet, basename='flat')

urlpatterns = [
    path('', include(router.urls))
]
