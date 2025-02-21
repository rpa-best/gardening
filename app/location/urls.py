from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'location', views.LocationView, "")
router.register(r'user', views.UserInLocationView, "")
router.register(r'invite', views.UserInLocationInviteView, "")
router.register(r'car', views.CarInLocationView, "")
router.register(r'location/(?P<cil_id>\d+)/history', views.HistoryLocationView, "")

urlpatterns = [
    path("", include(router.urls)),
    path("accept-invite/<uuid>/", views.CreateInviteView.as_view())
]