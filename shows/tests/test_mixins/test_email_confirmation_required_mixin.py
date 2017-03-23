from unittest.mock import MagicMock

from django.urls import reverse

from ...mixins import EmailConfirmationRequiredMixin


def test_it():
    user = MagicMock(is_confirmed=False)
    request = MagicMock()
    request.user = user
    response = EmailConfirmationRequiredMixin().dispatch(request)
    assert response.status_code == 302
    assert response.url == reverse('email-confirmation')