from unittest.mock import patch

import pytest

from ... import tasks
from ...models import Lottery

@pytest.mark.django_db
@patch('shows.broadway.get_captcha_id')
@patch('shows.broadway.get_g_recaptcha_response')
@patch('shows.broadway.enter_lottery')
def test_enter_user_in_lottery(_, __, ___, user, enterable_lottery):
    tasks.enter_user_in_lottery(user.id, enterable_lottery.id)
    enterable_lottery = Lottery.objects.get(id=enterable_lottery.id)
    assert enterable_lottery.entered_users.count() == 1
    assert enterable_lottery.entered_users.first() == user


