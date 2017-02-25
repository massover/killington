from django.db import models
from django.utils import timezone


class EnterableLotteryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            starts_at__lte=timezone.now(),
            ends_at__gt=timezone.now(),
            nonce__isnull=False,
            external_performance_id__isnull=False,
        )
