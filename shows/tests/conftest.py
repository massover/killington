from django.utils import timezone
from datetime import timedelta

import pytest
from pytest_factoryboy import register

from ..factories import (LotteryFactory, ShowFactory, PerformanceFactory,
                         UserFactory)

register(UserFactory)
register(ShowFactory)
register(PerformanceFactory)
register(LotteryFactory, 'active_lottery', processed=False,
         starts_at=timezone.now() - timedelta(minutes=30))


@pytest.fixture
def show__subscribed_users(user):
    return [user]
