import pytest

from shows.items import ShowItem
from ..spiders import ShowsSpider


def test_show_spider_parse(active_lottery_list_response):
    start_urls = ['http://example.com']
    spider = ShowsSpider(start_urls=start_urls)
    request = spider.parse(active_lottery_list_response)
    show_item = next(request).meta['show_item']

    assert show_item['lottery_ends_at'] == '9:00 am'
    assert show_item['performance_starts_at'] == '02/22/17 1:00 pm'
    assert show_item['url'] == 'https://lottery.broadwaydirect.com/show/aladdin/'


def test_show_spider_parse_callback(active_lottery_form_response):
    active_lottery_form_response.meta['show_item'] = ShowItem({
        'lottery_ends_at': '9:00 am',
        'performance_starts_at': '02/22/17 1:00 pm',
        'url': 'https://lottery.broadwaydirect.com/show/aladdin/',
    })

    start_urls = ['http://example.com']
    spider = ShowsSpider(start_urls=start_urls)
    show_item = spider.parse_callback(active_lottery_form_response)
    show_item = next(show_item)

    assert show_item['lottery_ends_at'] == '9:00 am'
    assert show_item['performance_starts_at'] == '02/22/17 1:00 pm'
    assert show_item['url'] == 'https://lottery.broadwaydirect.com/show/aladdin/'
    assert show_item['lottery_nonce'] == '72b5b8d688'
    assert show_item['lottery_external_performance_id'] == '209064'


def test_show_spider_parse(pending_lottery_list_response):
    start_urls = ['http://example.com']
    spider = ShowsSpider(start_urls=start_urls)
    show_item = spider.parse(pending_lottery_list_response)
    show_item = next(show_item)
    assert show_item['lottery_starts_at'] == '02/23/17 at 8:00 am'
    assert show_item['performance_starts_at'] == '02/23/17 7:00 pm'
    assert show_item['url'] == 'https://lottery.broadwaydirect.com/show/hamilton/'
