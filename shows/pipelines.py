from . import utils
from .models import Performance, Show, Lottery


class ShowPipeline(object):
    def process_item(self, item, spider):
        show = Show.objects.get(url=item['url'])
        performance, _ = Performance.objects.get_or_create(
            show=show,
            starts_at=utils.get_datetime_in_et(item['performance_starts_at'])
        )

        try:
            lottery = performance.lottery
        except Lottery.DoesNotExist:
            kwargs = {'performance': performance}
            if item.get('lottery_starts_at'):
                kwargs['starts_at'] = utils.get_datetime_in_et(item['lottery_starts_at'])
            if item.get('lottery_ends_at'):
                kwargs['ends_at'] = utils.get_datetime_in_et(item.get('lottery_ends_at'))

            lottery = Lottery.objects.create(**kwargs)
            return item

        if item.get('lottery_starts_at'):
            lottery.starts_at = utils.get_datetime_in_et(item['lottery_starts_at'])
        if item.get('lottery_ends_at'):
            lottery.ends_at = utils.get_datetime_in_et(item.get('lottery_ends_at'))

        lottery.save()

        return item
