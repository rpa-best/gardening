from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'location', views.LocationView, "")
router.register(r'location/(?P<location_id>\d+)/user', views.UserInLocationView, "")
router.register(r'location/(?P<location_id>\d+)/user/(?P<user_id>\d+)/car', views.UserInLocationCarView, "")
router.register(r'location/(?P<location_id>\d+)/invite', views.UserInLocationInviteView, "")
router.register(r'location/(?P<location_id>\d+)/car', views.CarInLocationView, "")
router.register(r'location/(?P<location_id>\d+)/camera', views.CameraInLocationView, "")

urlpatterns = [
    path("", include(router.urls)),
    path("invite/<uuid>/", views.CreateInviteView.as_view())
]