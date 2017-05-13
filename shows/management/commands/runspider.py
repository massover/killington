from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess

from ...spiders import ShowsSpider


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'ITEM_PIPELINES': {'shows.pipelines.ShowPipeline': 100}
        })
        process.crawl(ShowsSpider)
        process.start()
