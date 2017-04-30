from unittest.mock import patch

import requests
import pytest

from ... import broadway
from ... import constants
from ...exceptions import NoSlotAvailableError
from ...factories import LotteryFactory


@patch('requests.post')
def test_get_captcha_id(mock_post):
    response = requests.Response()
    response._content = 'OK|captcha-id'.encode()
    mock_post.return_value = response
    captcha_id = broadway.get_captcha_id(LotteryFactory.build())
    assert captcha_id == 'captcha-id'


@patch('requests.post')
@patch('time.sleep')
def test_no_slot_available_response_raises_exception(_, mock_post):
    response = requests.Response()
    response._content = constants.NO_SLOT_AVAILABLE_RESPONSE.encode()
    mock_post.return_value = response
    with pytest.raises(NoSlotAvailableError):
        broadway.get_captcha_id(LotteryFactory.build())
