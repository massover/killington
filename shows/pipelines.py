from django.utils import timezone

from .models import Performance, Show


class ShowPipeline(object):
    def process_item(self, item, spider):
        show = Show.objects.get(url=item['url'])
        performance, _ = Performance.objects.get_or_create(
            show=show,
            starts_at=item.get_datetime_in_et('performance_starts_at'),
        )

        lottery = performance.lottery

        lottery.starts_at = item.get_datetime_in_et(
            'lottery_starts_at',
            lottery.starts_at
        )
        if lottery.starts_at is None:
            lottery.starts_at = timezone.now()

        lottery.ends_at = item.get_datetime_in_et(
            'lottery_ends_at',
            lottery.ends_at
        )
        lottery.nonce = item.get('lottery_nonce', lottery.nonce)
        lottery.external_performance_id = item.get(
            'lottery_external_performance_id',
            lottery.external_performance_id
        )
        lottery.save()

        return item
