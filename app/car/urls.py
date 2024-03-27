from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarView

router = DefaultRouter()
router.register("car", CarView, "")

urlpatterns = [
    path("", include(router.urls))
]