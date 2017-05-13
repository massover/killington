import logging

import requests

logger = logging.getLogger(__name__)


def log_response(response):
    message = ('response.url: %s\n'
               'response.status_code: %s\n'
               'response.text: %s')
    logger.info(message, response.url, response.status_code, response.text)


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

    success_messages = [
        'Your lottery entry has been received!',
        'Before we can accept your entry, please check your email and click on the validation link provided.'
    ]

    if not any(message in response.text for message in success_messages):
        message = ('Lottery entry failed for user.id: {} '.format(user.id) +
                   'lottery.id: {}'.format(lottery.id))

        logger.warning(message)
        raise RuntimeError(message)
