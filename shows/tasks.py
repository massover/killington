from celery import shared_task
from .models import Lottery, User
from . import broadway


@shared_task()
def process_active_lotteries():
    for lottery in Lottery.active_objects.all():
        for user in lottery.performance.show.subscribed_users.all():
            enter_user_in_active_lottery.delay(lottery.id, user.id)
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
