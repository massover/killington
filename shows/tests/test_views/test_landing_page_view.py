from django.urls import reverse
import pytest

from ...models import User
from ..utils import fake


def test_get(client):
    response = client.get(reverse('landing-page'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_anonymous_user_required(client, user):
    client.login(username=user.username, password='password')
    response = client.get(reverse('landing-page'), follow=True)
    assert response.status_code == 200

    assert len(response.redirect_chain) == 1
    url, status_code = response.redirect_chain[0]
    assert url == reverse('subscriptions')
    assert status_code == 302


@pytest.mark.django_db
def test_post(client):
    data = {
        'full_name': fake.name(),
        'email': fake.email(),
        'zipcode': fake.zipcode(),
        'password': fake.password(),
        'date_of_birth': fake.date()
    }
    response = client.post(reverse('landing-page'), data=data)

    assert response.status_code == 302
    assert User.objects.count() == 1
