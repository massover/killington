from django.conf import settings
from django.urls import reverse


def test_it(client):
    response = client.get(reverse('acme-challenge'))
    assert response.status_code == 200
    assert response.content.decode() == settings.ACME_CHALLENGE_CONTENT