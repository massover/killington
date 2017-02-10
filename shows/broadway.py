from django.conf import settings

from time import sleep
import requests

CAPTCHA_IN_URL = 'http://2captcha.com/in.php'
CAPTCHA_RESULT_URL = 'http://2captcha.com/res.php'

def get_captcha_id(lottery):
    GOOGLE_CAPTCHA_SITE_KEY = '6LeIhQ4TAAAAACUkR1rzWeVk63ko-sACUlB7i932'
    params = {
        'key': settings.CAPTCHA_API_KEY,
        'method': 'userrecaptcha',
        'googlekey': GOOGLE_CAPTCHA_SITE_KEY,
        'pageurl': lottery.url,
    }
    response = requests.post(CAPTCHA_IN_URL, params=params)
    return response.text.split('|')[1]


def get_g_recaptcha_response(captcha_id):
    params = {
        'key': settings.CAPTCHA_API_KEY,
        'action': 'get',
        'id': captcha_id,
    }
    response = requests.get(CAPTCHA_RESULT_URL, params=params)
    while 'CAPCHA_NOT_READY' in response.text:
        sleep(5)
        response = requests.get(CAPTCHA_RESULT_URL, params=params)
    return response.text.split('|')[1]


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
        'dlslot_performance_id': lottery.lottery_id,
        'dlslot_nonce': lottery.nonce,
        '_wp_http_referer': lottery.http_referer,
    }
    headers = {'referer': lottery.url}
    response = requests.post(lottery.url, data=data, headers=headers)