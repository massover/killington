import os

from django.utils import timezone
from django.conf import settings
from datetime import timedelta

import pytest
from oauth2_provider.models import get_application_model, AccessToken
from pytest_factoryboy import register
from rest_framework.test import APIClient
from scrapy import Request
from scrapy.http import TextResponse

from ..factories import (LotteryFactory, ShowFactory, PerformanceFactory,
                         UserFactory)

register(UserFactory)
register(UserFactory, 'new_user')
register(ShowFactory)
register(PerformanceFactory)
register(LotteryFactory, 'enterable_lottery',
         starts_at=timezone.now() - timedelta(minutes=30),
         ends_at=timezone.now() + timedelta(minutes=30))


@pytest.fixture()
def api_client():
    Application = get_application_model()
    application = Application.objects.create(
        name="Test Application",
        redirect_uris="http://localhost",
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_IMPLICIT,
    )
    token = AccessToken.objects.create(
        token='1234567890',
        application=application,
        expires=timezone.now() + timedelta(days=1),
        scope='read',
    )
    api_client = APIClient()
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token))
    yield api_client


@pytest.fixture()
def user__subscribed_shows(show):
    yield [show]


@pytest.fixture
def active_lottery_list_response():
    url = 'https://lottery.broadwaydirect.com/show/aladdin/'
    request = Request(url=url)
    path = os.path.join(settings.BASE_DIR, 'shows/tests/html/active_lottery_list.html')
    with open(path) as fp:
        return TextResponse(
            url=url,
            request=request,
            body=fp.read(),
            encoding='utf-8'
        )


@pytest.fixture
def active_lottery_form_response():
    url = 'https://lottery.broadwaydirect.com/enter-lottery/?lottery=209064&window=popup'
    request = Request(url=url)
    path = os.path.join(settings.BASE_DIR, 'shows/tests/html/active_lottery_form.html')
    with open(path) as fp:
        return TextResponse(
            url=url,
            request=request,
            body=fp.read(),
            encoding='utf-8'
        )


@pytest.fixture
def pending_lottery_list_response():
    url = 'https://lottery.broadwaydirect.com/show/hamilton/'
    request = Request(url=url)
    path = os.path.join(settings.BASE_DIR, 'shows/tests/html/pending_lottery_list.html')
    with open(path) as fp:
        return TextResponse(
            url=url,
            request=request,
            body=fp.read(),
            encoding='utf-8'
        )
