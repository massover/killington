from unittest.mock import patch

import requests
import pytest

from ...factories import LotteryFactory, UserFactory
from ... import broadway


@patch('requests.post')
def test_it(mock_post):
    response = requests.Response()
    response._content = 'Your lottery entry has been received!'.encode()
    mock_post.return_value = response
    lottery = LotteryFactory.build()
    user = UserFactory.build()
    broadway.enter_lottery('g-recaptcha-response', lottery, user)


@patch('requests.post')
def test_it_raises_runtime_error_on_bad_response(mock_post):
    response = requests.Response()
    response._content = 'bad-response'.encode()
    mock_post.return_value = response
    lottery = LotteryFactory.build()
    user = UserFactory.build()
    with pytest.raises(RuntimeError):
        broadway.enter_lottery('g-recaptcha-response', lottery, user)