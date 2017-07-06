from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from ..models import SES
from .serializers import SESSerializer


class SESViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = SES.objects.all()
    lookup_field = 'email'
    lookup_value_regex = '(.+)'
    serializer_class = SESSerializer
    permission_classes = [TokenHasScope, ]
    required_scopes = ['read', ]
