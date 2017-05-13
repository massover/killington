from unittest.mock import patch

import pytest
import requests

from django.conf import settings

import toocy
from toocy.exceptions import NoSlotAvailableError
from shows.factories import LotteryFactory


@patch('requests.post')
def test_get_captcha_id(mock_post):
    response = requests.Response()
    response._content = 'OK|captcha-id'.encode()
    mock_post.return_value = response
    captcha_id = toocy.get_captcha_id(LotteryFactory.build())
    assert captcha_id == 'captcha-id'


@patch('requests.post')
@patch('time.sleep')
def test_no_slot_available_response_raises_exception(_, mock_post):
    response = requests.Response()
    response._content = settings.NO_SLOT_AVAILABLE_RESPONSE.encode()
    mock_post.return_value = response
    with pytest.raises(NoSlotAvailableError):
        toocy.get_captcha_id(LotteryFactory.build())
