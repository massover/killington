from datetime import timedelta
from django.utils import timezone

import pytest
from pytest_factoryboy import LazyFixture

from shows.factories import SESFactory
from ...models import Flood


@pytest.mark.django_db
def test_it(enterable_flood):
    assert Flood.enterable_objects.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize('enterable_lottery__starts_at',
                         [timezone.now() + timedelta(days=1)])
def test_it_ignores_future_lotteries(enterable_flood):
    assert Flood.enterable_objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('enterable_lottery__ends_at', [timezone.now()])
def test_it_ignores_past_lotteries(enterable_flood):
    assert Flood.enterable_objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('enterable_lottery__ends_at', [None])
def test_it_ignores_missing_ends_at(enterable_flood):
    assert Flood.enterable_objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('enterable_lottery__nonce', [None])
def test_it_ignores_missing_nonce(enterable_flood):
    assert Flood.enterable_objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('enterable_lottery__external_performance_id', [None])
def test_it_ignores_missing_external_performance_id(enterable_flood):
    assert Flood.enterable_objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('enterable_flood__entered_ses_set', [LazyFixture(lambda ses: [ses])])
def test_it_ignores_when_entered_ses_set_is_not_none(enterable_flood):
    enterable_flood.entered_ses_set.add(SESFactory())
    assert Flood.enterable_objects.count() == 0