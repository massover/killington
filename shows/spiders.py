import scrapy
from scrapy.loader import ItemLoader

from .models import Show
from .items import ShowItem


class ShowsSpider(scrapy.Spider):
    name = "shows"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('start_urls'):
            self.start_urls = kwargs['start_urls']
        else:
            self.start_urls = Show.objects.values_list('url', flat=True)

    def parse(self, response):
        for selector in response.css('.hide-for-tablets .lotteries-row'):
            show_item = ItemLoader(item=ShowItem(), selector=selector)
            show_item.add_value('url', response.url)
            show_item.add_css('performance_starts_at', '.lotteries-time::text')

            if selector.css('.lotteries-status').css('span.active'):
                show_item.add_css('lottery_ends_at', '.lotteries-status::text')
                next_page = selector.css('.lotteries-right a::attr(href)').extract_first()
                yield scrapy.Request(
                    next_page,
                    callback=self.parse_callback,
                    meta={'show_item': show_item.load_item()}
                )

            elif selector.css('.lotteries-status').css('span.pending'):
                show_item.add_css('lottery_starts_at', '.lotteries-status::text')
                yield show_item.load_item()

            elif selector.css('.lotteries-status').css('span.closed'):
                pass


    def parse_callback(self, response):
        show_item = response.meta['show_item']
        show_item = ItemLoader(item=show_item, response=response)
        show_item.add_xpath(
            'lottery_nonce',
            ".//input[starts-with(@id, 'dlslot_nonce')]/@value"
        )
        show_item.add_xpath(
            'lottery_external_performance_id',
            ".//input[starts-with(@name, 'dlslot_performance_id')]/@value"
        )
        yield show_item.load_item()

