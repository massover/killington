from datetime import timedelta, datetime

import pytest
import pytz
from django.utils import timezone

from shows.tests import utils
from ...items import ShowItem
from ...models import Performance, Lottery
from ...pipelines import ShowPipeline
from ...spiders import ShowsSpider


@pytest.mark.django_db
def test_it_creates_new_performances_and_pending_lottery(show):
    future = timezone.now() + timedelta(days=1)
    show_item = ShowItem({
        'url': show.url,
        'lottery_starts_at': future.strftime('%d/%m/%y at %I:%M %p'),
        'performance_starts_at': '02/23/17 7:00 pm'
    })
    pipeline = ShowPipeline()
    pipeline.process_item(show_item, ShowsSpider())

    assert Performance.objects.count() == 1

    performance = Performance.objects.first()
    assert performance.show == show

    starts_at = utils.get_datetime_in_et(show_item['performance_starts_at'])
    assert performance.starts_at == starts_at

    starts_at = utils.get_datetime_in_et(show_item['lottery_starts_at'])
    assert performance.lottery.starts_at == starts_at
    assert performance.lottery.ends_at is None
    assert performance.lottery.external_performance_id is None
    assert performance.lottery.nonce is None
    assert performance.lottery.state == Lottery.PENDING_STATE


@pytest.mark.django_db
def test_it_creates_new_performances_and_enterable_lottery(show):
    future = timezone.now() + timedelta(days=1)
    show_item = ShowItem({
        'url': show.url,
        'lottery_ends_at': future.strftime('%d/%m/%y at %I:%M %p'),
        'performance_starts_at': '02/23/17 7:00 pm',
        'lottery_nonce': '72b5b8d688',
        'lottery_external_performance_id': '209064',

    })
    pipeline = ShowPipeline()
    pipeline.process_item(show_item, ShowsSpider())

    assert Performance.objects.count() == 1

    performance = Performance.objects.first()
    assert performance.show == show

    starts_at = utils.get_datetime_in_et(show_item['performance_starts_at'])
    assert performance.starts_at == starts_at

    ends_at = utils.get_datetime_in_et(show_item['lottery_ends_at'])
    assert performance.lottery.ends_at == ends_at
    assert performance.lottery.nonce == '72b5b8d688'
    assert performance.lottery.external_performance_id == 209064
    assert performance.lottery.state == Lottery.ACTIVE_STATE


@pytest.mark.django_db
def test_it_gets_existing_performances_and_updates_existing_lotteries(show):
    past = datetime.now() - timedelta(days=1)
    past = past.replace(second=0, microsecond=0)
    eastern = pytz.timezone('US/Eastern')
    Performance.objects.create(show=show, starts_at=eastern.localize(past))

    future = timezone.now() + timedelta(days=1)
    show_item = ShowItem({
        'url': show.url,
        'lottery_ends_at': future.strftime('%d/%m/%y at %I:%M %p'),
        'performance_starts_at': past.strftime('%d/%m/%y at %I:%M %p'),
        'lottery_nonce': '72b5b8d688',
        'lottery_external_performance_id': '209064',
    })

    pipeline = ShowPipeline()
    pipeline.process_item(show_item, ShowsSpider())

    assert Performance.objects.count() == 1
    assert Lottery.objects.count() == 1

    performance = Performance.objects.first()
    assert performance.show == show

    starts_at = utils.get_datetime_in_et(show_item['performance_starts_at'])
    assert performance.starts_at == starts_at

    ends_at = utils.get_datetime_in_et(show_item['lottery_ends_at'])
    assert performance.lottery.ends_at == ends_at
    assert performance.lottery.nonce == '72b5b8d688'
    assert performance.lottery.external_performance_id == 209064
    assert performance.lottery.state == Lottery.ACTIVE_STATE
