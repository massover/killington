from datetime import timedelta
from django.utils import timezone

import pytest

from shows.models import Lottery


@pytest.mark.django_db
def test_it(enterable_lottery):
    assert Lottery.enterable_objects.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize('enterable_lottery__starts_at',
                         [timezone.now() + timedelta(days=1)])
def test_it_ignores_future_lotteries(enterable_lottery):
    assert Lottery.enterable_objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('enterable_lottery__ends_at', [timezone.now()])
def test_it_ignores_past_lotteries(enterable_lottery):
    assert Lottery.enterable_objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('enterable_lottery__ends_at', [None])
def test_it_ignores_missing_ends_at(enterable_lottery):
    assert Lottery.enterable_objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('enterable_lottery__nonce', [None])
def test_it_ignores_missing_nonce(enterable_lottery):
    assert Lottery.enterable_objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('enterable_lottery__external_performance_id', [None])
def test_it_ignores_missing_external_performance_id(enterable_lottery):
    assert Lottery.enterable_objects.count() == 0
