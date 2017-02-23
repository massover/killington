from celery import shared_task
from scrapy.crawler import CrawlerProcess

from .models import Lottery, User
from .spiders import ShowsSpider
from . import broadway


@shared_task()
def process_active_lotteries():
    for lottery in Lottery.active_objects.all():
        for user in lottery.performance.show.subscribed_users.all():
            enter_user_in_active_lottery.delay(user.id, lottery.id)
            lottery.entered_users.add(user)
        lottery.processed = True
        lottery.save()


@shared_task(max_retries=3)
def enter_user_in_active_lottery(user_id, lottery_id):
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