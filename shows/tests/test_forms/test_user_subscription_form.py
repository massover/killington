import pytest

from ...forms import UserSubscriptionForm


@pytest.mark.django_db
def test_all_fields(show):
    data = {'subscribed_shows': [str(show.id)], }
    form = UserSubscriptionForm(data=data)
    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_required_fields(show):
    data = {}
    form = UserSubscriptionForm(data=data)
    assert form.is_valid(), form.errors
