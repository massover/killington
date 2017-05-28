import logging
from datetime import timedelta

from billiard.exceptions import TimeLimitExceeded
from celery import shared_task
from requests import RequestException
from scrapy.crawler import CrawlerProcess

import toocy
from toocy.exceptions import NoSlotAvailableError
from . import broadway
from .models import Lottery, User, Flood, SES
from .spiders import ShowsSpider

logger = logging.getLogger(__name__)

AUTORETRY_FOR_EXCEPTIONS = (NoSlotAvailableError, TimeoutError, RuntimeError,
                            RequestException, TimeLimitExceeded)


@shared_task()
def process_enterable_lotteries():
    for lottery in Lottery.enterable_objects.all():
        for user in lottery.performance.show.subscribed_users.filter(is_active=True):
            if user.entered_lotteries.filter(id=lottery.id).exists():
                continue
            enter_user_in_lottery.delay(user.id, lottery.id)


@shared_task(max_retries=3, autoretry_for=AUTORETRY_FOR_EXCEPTIONS)
def enter_user_in_lottery(user_id, lottery_id):
    message = 'Entering user.id: {} in lottery.id: {}'.format(
        user_id,
        lottery_id
    )
    logger.info(message)

    # If a task took too long to get processed, the lottery may be not
    # be enterable anymore, so just exit.
    try:
        lottery = Lottery.enterable_objects.get(id=lottery_id)
    except Lottery.DoesNotExist:
        return

    captcha_id = toocy.get_captcha_id(lottery)
    g_recaptcha_response = toocy.get_g_recaptcha_response(captcha_id)

    user = User.objects.get(id=user_id)
    broadway.enter_lottery(g_recaptcha_response, lottery, user)
    lottery.entered_users.add(user)


@shared_task(max_retries=3, autoretry_for=AUTORETRY_FOR_EXCEPTIONS)
def enter_user_in_lottery_for_flood(flood_id, ses_id, date_of_birth_offset):
    flood = Flood.objects.get(id=flood_id)
    message = 'Flood entry for ses.id: {} in lottery.id: {}'.format(
        ses_id,
        flood.lottery.id,
    )
    logger.info(message)

    # If a task took too long to get processed, the lottery may be not
    # be enterable anymore, so just exit.
    try:
        lottery = Lottery.enterable_objects.get(id=flood.lottery.id)
    except Lottery.DoesNotExist:
        return

    captcha_id = toocy.get_captcha_id(lottery)
    g_recaptcha_response = toocy.get_g_recaptcha_response(captcha_id)

    ses = SES.objects.get(id=ses_id)
    user = User(
        first_name=ses.user.first_name,
        last_name=ses.user.last_name,
        zipcode=ses.user.zipcode,
        email=ses.email,
        date_of_birth=ses.user.date_of_birth + timedelta(days=date_of_birth_offset),
    )
    broadway.enter_lottery(g_recaptcha_response, lottery, user)

    flood.entered_ses_set.add(ses)


@shared_task
def run_shows_spider(*args, **kwargs):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ITEM_PIPELINES': {'shows.pipelines.ShowPipeline': 100}
    })
    process.crawl(ShowsSpider, *args, **kwargs)
    process.start()


@shared_task
def process_enterable_floods():
    for flood in Flood.enterable_objects.all():
        for index, ses in enumerate(flood.client.ses_set.all()):
            enter_user_in_lottery_for_flood.delay(
                flood.id,
                ses.id,
                index
            )
