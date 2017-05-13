from django.conf.urls import url, include
from rest_framework import routers

from . import viewsets

router = routers.SimpleRouter()
router.register(r'ses', viewsets.SESViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
