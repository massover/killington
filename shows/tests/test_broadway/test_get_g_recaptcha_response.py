from unittest.mock import patch
import pytest

from ... import broadway
import requests


@patch('requests.get')
def test_it_raises_a_timeout_error(mock_get):
    with pytest.raises(TimeoutError):
        broadway.get_g_recaptcha_response('captcha-id')


@patch('requests.get')
def test_it(mock_get):
    response = requests.Response()
    response._content = 'OK|g-recaptcha-response'.encode()
    mock_get.return_value = response
    g_recaptcha_response = broadway.get_g_recaptcha_response('captcha-id')
    assert g_recaptcha_response == 'g-recaptcha-response'
