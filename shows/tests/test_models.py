from datetime import timedelta, datetime

from django.core.exceptions import ValidationError
from django.utils import timezone
import pytest

from ..factories import LotteryFactory
from ..models import Lottery, Performance


@pytest.mark.django_db
def test_performance_post_save(show):
    performance = Performance.objects.create(
        show=show,
        starts_at=timezone.now(),
    )
    assert performance.lottery is not None


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
        starts_at=timezone.now() - timedelta(hours=2),
        ends_at=None,
    )
    assert lottery.state == Lottery.INVALID_STATE


def test_lottery_clean_starts_at_must_not_equal_ends_at():
    lottery = LotteryFactory.build(
        starts_at=datetime(2000, 1, 1),
        ends_at=datetime(2000, 1, 1),
    )
    with pytest.raises(ValidationError):
        lottery.clean()


def test_lottery_clean_starts_at_must_be_before_ends_at():
    lottery = LotteryFactory.build(
        starts_at=datetime(3000, 3, 3),
        ends_at=datetime(2000, 1, 1),
    )

    with pytest.raises(ValidationError):
        lottery.clean()


def test_lottery_clean_allows_empty_ends_at():
    lottery = LotteryFactory.build(
        starts_at=datetime(3000, 3, 3),
        ends_at=None,
    )
    lottery.clean()