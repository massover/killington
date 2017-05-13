import pytz
from faker import Faker
from dateutil.parser import parse


def get_datetime_in_et(timestr):
    eastern = pytz.timezone('US/Eastern')
    return eastern.localize(parse(timestr))


fake = Faker()
