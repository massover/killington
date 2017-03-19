from django.contrib.auth import get_user_model
from django.urls import reverse
import pytest

from ..utils import fake


def test_get(client):
    response = client.get(reverse('landing-page'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_anonymous_user_required(client, user):
    client.login(email=user.email, password='password')
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
        'date_of_birth': '1989-01-01',
    }
    response = client.post(reverse('landing-page'), data=data, follow=True)
    assert response.status_code == 200

    assert len(response.redirect_chain) == 1
    url, status_code = response.redirect_chain[0]
    assert url == reverse('subscriptions')
    assert status_code == 302

    User = get_user_model()
    assert User.objects.count() == 1
    assert client.session['_auth_user_id'] == str(User.objects.first().id)
