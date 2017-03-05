import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_it_redirects_logged_in_users(client, user):
    client.login(username=user.username, password='password')
    response = client.get(reverse('login'), follow=True)
    assert response.status_code == 200

    assert len(response.redirect_chain) == 1
    url, status_code = response.redirect_chain[0]
    assert url == reverse('subscriptions')
    assert status_code == 302


@pytest.mark.django_db
def test_it(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_it_logs_users_in(client, user):
    data = {
        'username': user.username,
        'password': 'password'
    }
    response = client.post(reverse('login'), data=data, follow=True)
    assert response.status_code == 200

    assert len(response.redirect_chain) == 1
    url, status_code = response.redirect_chain[0]
    assert url == reverse('subscriptions')
    assert status_code == 302

