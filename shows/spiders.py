import pytz

from dateutil.parser import parse
import scrapy
from .models import Performance, Lottery, Show


class ShowsSpider(scrapy.Spider):
    name = "shows"

    def __init__(self, *args, **kwargs):
        super(ShowsSpider, self).__init__(*args, **kwargs)
        if kwargs.get('queryset'):
            self.start_urls = kwargs['queryset'].values_list('url', flat=True)
        else:
            self.start_urls = Show.objects.values_list('url', flat=True)

    def parse(self, response):
        show = Show.objects.get(url=response.url)
        eastern = pytz.timezone('US/Eastern')

        for lottery_row in response.css('.hide-for-tablets .lotteries-row'):
            raw_performace_starts_at = lottery_row.css('.lotteries-time::text').extract_first()
            performance_starts_at_utc = parse(raw_performace_starts_at.strip())

            # 02/18/17 8:00 pm
            performance, _ = Performance.objects.get_or_create(
                show=show,
                starts_at=eastern.localize(performance_starts_at_utc)
            )

            if lottery_row.css('.lotteries-status').css('span.active'):
                raw_lottery_ends_at = lottery_row.css('.lotteries-status::text').extract()[2]
                lottery_ends_at = raw_lottery_ends_at.split('Closes at')[1]
                lottery_ends_at_utc = parse(lottery_ends_at.strip())

                # Closes at 2:00 pm
                lottery, _ = Lottery.objects.get_or_create(
                    performance=performance,
                    ends_at=eastern.localize(lottery_ends_at_utc)
                )

                next_page = lottery_row.css('.lotteries-right a::attr(href)').extract_first()
                request = scrapy.Request(next_page, callback=self.parse_lottery)
                request.meta['lottery'] = lottery
                yield request

            elif lottery_row.css('.lotteries-status').css('span.pending'):
                raw_lottery_starts_at = lottery_row.css('.lotteries-status::text').extract()[1]
                lottery_starts_at_utc = parse(raw_lottery_starts_at.strip())
                # 02/18/17 at 11:00 am

                lottery, _ = Lottery.objects.get_or_create(
                    performance=performance,
                    starts_at=eastern.localize(lottery_starts_at_utc)
                )

            elif lottery_row.css('.lotteries-status').css('span.closed'):
                pass


    def parse_lottery(self, response):
        lottery = response.meta['lottery']
        nonce = response.xpath(
            ".//input[starts-with(@id, 'dlslot_nonce')]/@value"
        ).extract_first()
        if lottery.nonce != nonce:
            lottery.nonce = nonce


        external_performance_id = response.xpath(
            ".//input[starts-with(@name, 'dlslot_performance_id')]/@value"
        ).extract_first()
        if lottery.external_performance_id != external_performance_id:
            lottery.external_performance_id = external_performance_id

        lottery.save()
