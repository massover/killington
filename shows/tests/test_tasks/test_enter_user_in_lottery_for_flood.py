from unittest.mock import patch

from django.utils import timezone
import pytest

from ... import tasks
from ...models import Flood


@pytest.mark.django_db
@patch('shows.broadway.get_captcha_id')
@patch('shows.broadway.get_g_recaptcha_response')
@patch('shows.broadway.enter_lottery')
def test_it(_, __, ___, flood_user, enterable_flood):
    ses = flood_user.ses_set.first()
    date_of_birth_offset = 1
    tasks.enter_user_in_lottery_for_flood(enterable_flood.id, ses.id, date_of_birth_offset)
    enterable_flood = Flood.objects.get(id=enterable_flood.id)
    assert enterable_flood.entered_ses_set.count() == 1
    assert enterable_flood.entered_ses_set.first() == flood_user.ses_set.first()


@pytest.mark.django_db
@pytest.mark.parametrize('enterable_lottery__ends_at', [timezone.now()])
def test_it_will_not_enter_users_when_lottery_is_not_enterable(flood_user, enterable_flood):
    ses = flood_user.ses_set.first()
    date_of_birth_offset = 1
    tasks.enter_user_in_lottery_for_flood(enterable_flood.id, ses.id, date_of_birth_offset)
    enterable_flood = Flood.objects.get(id=enterable_flood.id)
    assert enterable_flood.entered_ses_set.count() == 0