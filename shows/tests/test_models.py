from datetime import timedelta, datetime

from django.core.exceptions import ValidationError
from django.utils import timezone
import pytest

from ..factories import LotteryFactory
from ..models import Lottery


def test_lottery_url():
    lottery = LotteryFactory.build()
    assert str(lottery.external_performance_id) in lottery.url


def test_lottery_http_referer():
    lottery = LotteryFactory.build()
    assert str(lottery.external_performance_id) in lottery.http_referer


def test_pending_lottery_state():
    lottery = LotteryFactory.build(
        starts_at=timezone.now() + timedelta(hours=1),
        ends_at=timezone.now() + timedelta(hours=2),
    )
    assert lottery.state == Lottery.PENDING_STATE


def test_active_lottery_state():
    lottery = LotteryFactory.build(
        starts_at=timezone.now() - timedelta(hours=1),
        ends_at=timezone.now() + timedelta(hours=1),
    )
    assert lottery.state == Lottery.ACTIVE_STATE


def test_closed_lottery_state():
    lottery = LotteryFactory.build(
        starts_at=timezone.now() - timedelta(hours=2),
        ends_at=timezone.now() - timedelta(hours=1),
    )
    assert lottery.state == Lottery.CLOSED_STATE


def test_invalid_lottery_state():
    lottery = LotteryFactory.build(
        starts_at=datetime(2000, 1, 1),
        ends_at=datetime(2000, 1, 1),
    )

    with pytest.raises(ValidationError):
        lottery.clean()


def test_lottery_starts_at_must_be_before_ends_at():
    lottery = LotteryFactory.build(
        starts_at=timezone.now() - timedelta(hours=2),
        ends_at=None,
    )
    assert lottery.state == Lottery.INVALID_STATE


@pytest.mark.django_db
def test_lottery_starts_at_has_default_value(performance):
    lottery = Lottery.objects.create(performance=performance)
    assert isinstance(lottery.starts_at, datetime)


def test_lottery_starts_at_must_not_equal_ends_at():
    lottery = LotteryFactory.build(
        starts_at=datetime(2000, 1, 1),
        ends_at=datetime(2000, 1, 1),
    )
    with pytest.raises(ValidationError):
        lottery.clean()
