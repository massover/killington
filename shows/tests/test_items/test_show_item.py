from ...items import ShowItem


def test_get_datetime_in_et():
    show_item = ShowItem({'performance_starts_at': '02/23/17 7:00 pm'})

    datetime = show_item.get_datetime_in_et('performance_starts_at')
    assert datetime.year == 2017
    assert datetime.tzinfo.zone == 'US/Eastern'
