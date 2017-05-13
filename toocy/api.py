import datetime
import time
import requests
from django.conf import settings

from shows.broadway import log_response
from toocy.exceptions import NoSlotAvailableError


def get_captcha_id(lottery):
    params = {
        'key': settings.CAPTCHA_API_KEY,
        'method': 'userrecaptcha',
        'googlekey': settings.GOOGLE_CAPTCHA_SITE_KEY,
        'pageurl': lottery.url,
    }
    response = requests.post(settings.CAPTCHA_IN_URL, params=params)
    log_response(response)
    if settings.NO_SLOT_AVAILABLE_RESPONSE in response.text:
        time.sleep(settings.NO_SLOT_AVAILABLE_RETRY_DELAY)
        message = 'No recaptcha slot available for lottery.id: {}'.format(lottery.id)
        raise NoSlotAvailableError(message)

    time.sleep(settings.AFTER_CAPTCHA_UPLOAD_REQUEST_DELAY)
    return response.text.split('|')[1]


def get_g_recaptcha_response(captcha_id):
    params = {
        'key': settings.CAPTCHA_API_KEY,
        'action': 'get',
        'id': captcha_id,
    }
    start_time = datetime.datetime.now()
    while True:
        response = requests.get(settings.CAPTCHA_RESULT_URL, params=params)
        log_response(response)
        if 'OK' in response.text:
            return response.text.split('|')[1]

        time_elapsed = datetime.datetime.now() - start_time
        if time_elapsed.seconds > settings.G_RECAPTCHA_RESPONSE_TIMEOUT:
            raise TimeoutError('Timeout on google recaptcha response')

        time.sleep(settings.G_RECAPTCHA_RESPONSE_RETRY_DELAY)