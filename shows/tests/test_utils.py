from shows.tests import utils


def test_get_datetime_in_et():
    datetime = utils.get_datetime_in_et('02/23/17 at 8:00 am')
    assert datetime.month == 2
    assert datetime.day == 23
    assert datetime.year == 2017
    assert datetime.tzinfo.zone == 'US/Eastern'