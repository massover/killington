from unittest.mock import patch

import requests

from ... import broadway
from ...factories import LotteryFactory


@patch('requests.post')
def test_get_captcha_id(mock_post):
    response = requests.Response()
    response._content = 'OK|captcha-id'.encode()
    mock_post.return_value = response
    captcha_id = broadway.get_captcha_id(LotteryFactory.build())
    assert captcha_id == 'captcha-id'
