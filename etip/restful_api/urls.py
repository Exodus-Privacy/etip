from django.urls import include, path
from rest_framework import routers

from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = routers.DefaultRouter()
router.register(r'trackers', views.TrackerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('get-auth-token/', obtain_auth_token)
]
