import pytest

from django.conf import settings

from ...models import SES


@pytest.mark.django_db
def test_bulk_create_with_random_emails_for_user(user):
    SES.objects.bulk_create_with_random_emails_for_user(user, num_objects=1)
    assert user.ses_set.count() == 1
    assert user.ses_set.first().email.endswith(settings.SES_DOMAIN)