import pytest

from ...models import User
from ...factories import UserFactory


@pytest.mark.django_db
def test_get_by_natural_key_is_case_insensitive():
    user = UserFactory(email='user@example.com')
    found_user = User.objects.get_by_natural_key('USER@EXAMPLE.COM')
    assert found_user == user
