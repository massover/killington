import logging

from celery import shared_task
from scrapy.crawler import CrawlerProcess

from .models import Lottery, User
from .spiders import ShowsSpider
from . import broadway

logger = logging.getLogger(__name__)

@shared_task()
def process_enterable_lotteries():
    for lottery in Lottery.enterable_objects.all():
        for user in lottery.performance.show.subscribed_users.all():
            if user.entered_lotteries.filter(id=lottery.id).exists():
                continue
            enter_user_in_lottery.delay(user.id, lottery.id)


@shared_task(max_retries=3)
def enter_user_in_lottery(user_id, lottery_id):
    message = 'Entering user.id: {} in lottery.id: {}'.format(
        user_id,
        lottery_id
    )
    logger.info(message)
    lottery = Lottery.objects.get(id=lottery_id)
    captcha_id = broadway.get_captcha_id(lottery)
    g_recaptcha_response = broadway.get_g_recaptcha_response(captcha_id)

    user = User.objects.get(id=user_id)
    broadway.enter_lottery(g_recaptcha_response, lottery, user)
    lottery.entered_users.add(user)


@shared_task
def run_shows_spider(*args, **kwargs):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ITEM_PIPELINES':  {'shows.pipelines.ShowPipeline': 100}
    })
    process.crawl(ShowsSpider, *args, **kwargs)
    process.start()