import pytest

from django.urls import reverse
from django.core import mail

from ...models import User


@pytest.mark.django_db
def test_get(client, user):
    client.login(email=user.email, password='password')
    response = client.get(reverse('email-confirmation'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_updates_confirmation_code_and_sends_email(client, user):
    old_confirmation_code = user.confirmation_code
    client.login(email=user.email, password='password')
    response = client.post(reverse('email-confirmation'))

    user = User.objects.get(id=user.id)
    assert response.status_code == 302
    assert user.confirmation_code != old_confirmation_code
    assert len(mail.outbox) == 1
    assert isinstance(user.confirmation_code, str)


def test_login_required(client):
    response = client.get(reverse('email-confirmation'))
    assert response.status_code == 302
