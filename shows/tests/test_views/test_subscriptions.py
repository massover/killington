from django.conf import settings
from django.urls import reverse
import pytest


def test_login_is_required(client):
    response = client.get(reverse('subscriptions'), follow=True)
    assert response.status_code == 200

    assert len(response.redirect_chain) == 1
    url, status_code = response.redirect_chain[0]
    login_url = settings.LOGIN_URL + \
        '?next={}'.format(reverse('subscriptions'))
    assert url == login_url


@pytest.mark.django_db
def test_unsubscribe_from_all(client, user):
    client.login(email=user.email, password='password')
    data = {'button': 'unsubscribe-from-all'}
    response = client.post(
        reverse('subscriptions'),
        follow=True,
        data=data
    )
    assert response.status_code == 200
    assert user.subscribed_shows.count() == 0


@pytest.mark.django_db
def test_unsubscribe_from_show(client, user):
    client.login(email=user.email, password='password')
    data = {'button': 'update-subscriptions',
            'subscribed_shows': []}
    response = client.post(
        reverse('subscriptions'),
        follow=True,
        data=data
    )
    assert response.status_code == 200
    assert user.subscribed_shows.count() == 0


@pytest.mark.django_db
def test_subscribe_to_show(client, new_user, show):
    client.login(email=new_user.email, password='password')
    data = {
        'button': 'update-subscriptions',
        'subscribed_shows': [str(show.id)],
    }
    response = client.post(
        reverse('subscriptions'),
        follow=True,
        data=data
    )
    assert response.status_code == 200
    assert new_user.subscribed_shows.count() == 1
