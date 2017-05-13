from unittest.mock import patch

from django.utils import timezone
import pytest

from ... import tasks
from ...models import Lottery


@pytest.mark.django_db
@patch('toocy.get_captcha_id')
@patch('toocy.get_g_recaptcha_response')
@patch('shows.broadway.enter_lottery')
def test_it(_, __, ___, user, enterable_lottery):
    tasks.enter_user_in_lottery(user.id, enterable_lottery.id)
    enterable_lottery = Lottery.objects.get(id=enterable_lottery.id)
    assert enterable_lottery.entered_users.count() == 1
    assert enterable_lottery.entered_users.first() == user


@pytest.mark.django_db
@pytest.mark.parametrize('enterable_lottery__ends_at', [timezone.now()])
def test_it_will_not_enter_users_when_lottery_is_not_enterable(user, enterable_lottery):
    tasks.enter_user_in_lottery(user.id, enterable_lottery.id)
    enterable_lottery = Lottery.objects.get(id=enterable_lottery.id)
    assert enterable_lottery.entered_users.count() == 0
