from datetime import timedelta, datetime

import pytest
import pytz
from django.utils import timezone

from .. import utils
from ..items import ShowItem
from ..pipelines import ShowPipeline
from ..spiders import ShowsSpider
from ..models import Performance, Lottery
from ..factories import PerformanceFactory


@pytest.mark.django_db
def test_show_pipeline_creates_new_performances_and_pending_lottery(show):
    show_item = ShowItem({
        'url': show.url,
        'lottery_starts_at': '02/23/17 at 8:00 am',
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
    assert performance.lottery.state == Lottery.PENDING_STATE


@pytest.mark.django_db
def test_show_pipeline_creates_new_performances_and_active_lottery(show):
    future = timezone.now() + timedelta(days=1)
    show_item = ShowItem({
        'url': show.url,
        'lottery_ends_at': future.strftime('%d/%m/%y at %I:%M %p'),
        'performance_starts_at': '02/23/17 7:00 pm',
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
    assert performance.lottery.state == Lottery.ACTIVE_STATE


@pytest.mark.django_db
def test_show_pipeline_gets_existing_performances_and_updates_existing_lotteries(show):
    past = datetime.now() - timedelta(days=1)
    past = past.replace(second=0, microsecond=0)
    eastern = pytz.timezone('US/Eastern')
    PerformanceFactory(show=show, starts_at=eastern.localize(past))

    future = timezone.now() + timedelta(days=1)
    show_item = ShowItem({
        'url': show.url,
        'lottery_ends_at': future.strftime('%d/%m/%y at %I:%M %p'),
        'performance_starts_at': past.strftime('%d/%m/%y at %I:%M %p'),
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
    assert performance.lottery.state == Lottery.ACTIVE_STATE
