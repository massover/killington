import pytest

from django.urls import reverse

from ...models import User


@pytest.mark.django_db
@pytest.mark.parametrize('user__is_confirmed', [False])
def test_it_returns_400_on_bad_confirmation_code(client, user):
    client.login(email=user.email, password='password')
    kwargs = {'confirmation_code': 'badcode'}
    url = reverse('email-confirmation-code-validation', kwargs=kwargs)
    response = client.get(url)
    assert response.status_code == 400


@pytest.mark.django_db
@pytest.mark.parametrize('user__is_confirmed', [False])
def test_post_updates_confirmation_code(client, user):
    client.login(email=user.email, password='password')
    kwargs = {'confirmation_code': user.confirmation_code}
    url = reverse('email-confirmation-code-validation', kwargs=kwargs)
    response = client.get(url)

    user = User.objects.get(id=user.id)
    assert response.status_code == 302
    assert user.is_confirmed is True


def test_login_required(client):
    kwargs = {'confirmation_code': 'confirmation_code'}
    url = reverse('email-confirmation-code-validation', kwargs=kwargs)
    response = client.get(url)
    assert response.status_code == 302