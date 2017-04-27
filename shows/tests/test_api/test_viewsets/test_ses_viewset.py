import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from ....factories import UserFactory, SESFactory


@pytest.mark.django_db
def test_it(api_client):
    user = UserFactory(email='user@example.com')
    ses = SESFactory(user=user)
    response = api_client.get(reverse('ses-detail', kwargs={'email': ses.email}))
    assert response.status_code == 200
    assert response.json()['user']['email'] == user.email


@pytest.mark.django_db
def test_it_requires_authentication():
    client = APIClient()
    user = UserFactory(email='user@example.com')
    ses = SESFactory(user=user)
    response = client.get(reverse('ses-detail', kwargs={'email': ses.email}))
    print(response.json())
    assert response.status_code == 401


