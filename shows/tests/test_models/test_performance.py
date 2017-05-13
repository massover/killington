from django.utils import timezone
import pytest

from ...models import Performance


@pytest.mark.django_db
def test_performance_post_save(show):
    performance = Performance.objects.create(
        show=show,
        starts_at=timezone.now(),
    )
    assert performance.lottery is not None
