import scrapy
from scrapy.loader.processors import TakeFirst, Join, MapCompose


def remove_closes_at(value):
    return value.replace('Closes at ', '')


class ShowItem(scrapy.Item):
    performance_starts_at = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=Join(separator='')
    )
    lottery_starts_at = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=Join(separator=''),
    )
    lottery_ends_at = scrapy.Field(
        input_processor=MapCompose(str.strip, remove_closes_at),
        output_processor=Join(separator=''),
    )
    lottery_nonce = scrapy.Field(output_processor=TakeFirst())
    lottery_external_performance_id = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
