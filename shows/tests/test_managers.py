from datetime import timedelta
from django.utils import timezone

import pytest

from shows.models import Lottery


@pytest.mark.django_db
def test_active_lottery_manager(active_lottery):
    assert Lottery.active_objects.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize('active_lottery__processed', [True])
def test_active_lottery_manager_ignores_processed_lotteries(active_lottery):
    assert Lottery.active_objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('active_lottery__starts_at',
                         [timezone.now() + timedelta(days=1)])
def test_active_lottery_manager_ignores_future_lotteries(active_lottery):
    assert Lottery.active_objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('active_lottery__ends_at', [timezone.now()])
def test_active_lottery_manager_ignores_past_lotteries(active_lottery):
    assert Lottery.active_objects.count() == 0
