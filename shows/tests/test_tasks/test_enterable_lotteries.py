from unittest.mock import patch

import pytest
from pytest_factoryboy import LazyFixture

from ... import tasks
from ...models import Lottery


@pytest.mark.django_db
@patch('toocy.get_captcha_id')
@patch('toocy.get_g_recaptcha_response')
@patch('shows.broadway.enter_lottery')
def test_it(_, __, ___, enterable_lottery):
    tasks.process_enterable_lotteries()

    enterable_lottery = Lottery.objects.get(id=enterable_lottery.id)
    entered_users = enterable_lottery.entered_users
    subscribed_users = enterable_lottery.performance.show.subscribed_users
    assert entered_users.count() == subscribed_users.count()


@pytest.mark.django_db
@pytest.mark.parametrize('enterable_lottery__entered_users',
                         [LazyFixture(lambda user: [user])])
@patch('shows.tasks.enter_user_in_lottery.delay')
def test_it_skips_users_that_were_already_entered(mock, enterable_lottery):
    tasks.process_enterable_lotteries()

    assert not mock.called
