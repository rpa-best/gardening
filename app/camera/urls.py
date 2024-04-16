from django.urls import path
from .views import RegisterView, CameraOpenView


urlpatterns = [
    path("register-history/", RegisterView.as_view()),
    path("camera/<id>/open/", CameraOpenView.as_view())
]