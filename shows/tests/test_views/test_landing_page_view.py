from django.urls import reverse
import pytest

from ...models import User
from ..utils import fake


def test_get(client):
    response = client.get(reverse('landing-page'))
    assert response.status_code == 200


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

    assert response.status_code == 302, response.content.decode()
    assert User.objects.count() == 1
