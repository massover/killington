from unittest.mock import MagicMock

from django.urls import reverse

from ...mixins import AnonymousRequiredMixin


def test_it():
    user = MagicMock(is_authenticated=True)
    request = MagicMock()
    request.user = user
    response = AnonymousRequiredMixin().dispatch(request)
    assert response.status_code == 302
    assert response.url == reverse('subscriptions')
