from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'location', views.LocationView, "")
router.register(r'location/(?P<location_id>\d+)/user', views.UserInLocationView, "")
router.register(r'location/(?P<location_id>\d+)/user/(?P<user_id>\d+)/car', views.UserInLocationCarView, "")
router.register(r'location/(?P<location_id>\d+)/invite', views.UserInLocationInviteView, "")
router.register(r'location/(?P<location_id>\d+)/car', views.CarInLocationView, "")

urlpatterns = [
    path("", include(router.urls))
]