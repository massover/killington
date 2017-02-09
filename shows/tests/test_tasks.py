from unittest.mock import patch

import pytest

from ..models import Lottery
from .. import tasks

@pytest.mark.django_db
@patch('shows.tasks.enter_user_in_active_lottery')
def test_process_active_lotteries(_, active_lottery):
    tasks.process_active_lotteries()
    active_lottery = Lottery.objects.get(id=active_lottery.id)
    assert active_lottery.processed is True

    entered_users = active_lottery.entered_users
    subscribed_users = active_lottery.performance.show.subscribed_users
    assert entered_users.count() == subscribed_users.count()


@pytest.mark.django_db
@patch('shows.broadway.get_captcha_id')
@patch('shows.broadway.get_g_recaptcha_response')
@patch('shows.broadway.enter_lottery')
def test_enter_user_in_active_lottery(_, __, ___, user, active_lottery):
    tasks.enter_user_in_active_lottery(user.id, active_lottery.id)
    active_lottery = Lottery.objects.get(id=active_lottery.id)
    assert active_lottery.entered_users.count() == 1
    assert active_lottery.entered_users.first() == user

