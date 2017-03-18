import logging
import datetime

from django.conf import settings

from time import sleep
import requests

CAPTCHA_IN_URL = 'http://2captcha.com/in.php'
CAPTCHA_RESULT_URL = 'http://2captcha.com/res.php'

logger = logging.getLogger(__name__)


def log_response(response):
    message = ('response.url: %s\n'
               'response.status_code: %s\n'
               'response.text: %s')
    logger.info(message, response.url, response.status_code, response.text)


def get_captcha_id(lottery):
    GOOGLE_CAPTCHA_SITE_KEY = '6LeIhQ4TAAAAACUkR1rzWeVk63ko-sACUlB7i932'
    params = {
        'key': settings.CAPTCHA_API_KEY,
        'method': 'userrecaptcha',
        'googlekey': GOOGLE_CAPTCHA_SITE_KEY,
        'pageurl': lottery.url,
    }
    response = requests.post(CAPTCHA_IN_URL, params=params)
    log_response(response)
    return response.text.split('|')[1]


def get_g_recaptcha_response(captcha_id):
    params = {
        'key': settings.CAPTCHA_API_KEY,
        'action': 'get',
        'id': captcha_id,
    }
    start_time = datetime.datetime.now()
    while True:
        response = requests.get(CAPTCHA_RESULT_URL, params=params)
        log_response(response)
        if 'OK' in response.text:
            return response.text.split('|')[1]

        time_elapsed = datetime.datetime.now() - start_time
        if time_elapsed.seconds > settings.CAPTCHA_TIMEOUT:
            raise TimeoutError('Timeout on google recaptcha response')

        sleep(5)


def enter_lottery(g_recaptcha_response, lottery, user):
    data = {
        'dlslot_name_first': user.first_name,
        'dlslot_name_last': user.last_name,
        'dlslot_ticket_qty': 2,
        'dlslot_email': user.email,
        'dlslot_dob_month': user.date_of_birth.month,
        'dlslot_dob_day': user.date_of_birth.day,
        'dlslot_dob_year': user.date_of_birth.year,
        'dlslot_zip': user.zipcode,
        'dlslot_agree': True,
        'dlslot_country': 2,
        'g-recaptcha-response': g_recaptcha_response,
        'dlslot_website': '',
        'dlslot_performance_id': lottery.external_performance_id,
        'dlslot_nonce': lottery.nonce,
        '_wp_http_referer': lottery.http_referer,
    }
    headers = {'referer': lottery.url}
    response = requests.post(lottery.url, data=data, headers=headers)
    log_response(response)

    if 'Your lottery entry has been received!' not in response.text:
        message = ('Lottery entry failed for user.id: {} '.format(user.id) +
                   'lottery.id: {}'.format(lottery.id))
        logger.warning(message)
        raise RuntimeError(message)