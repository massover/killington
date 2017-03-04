import factory
import pytz
from django.db.models import signals

from .models import Lottery, Performance, Show, User


class UserFactory(factory.DjangoModelFactory):
    date_of_birth = factory.Faker('date')
    zipcode = factory.Faker('zipcode')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    username = factory.Faker('pystr')
    is_superuser = factory.Faker('pybool')
    is_staff = factory.Faker('pybool')
    password = factory.PostGenerationMethodCall('set_password', 'password')
    subscribed_shows = factory.RelatedFactory('shows.factories.ShowFactory')

    @factory.post_generation
    def subscribed_shows(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for subscribed_show in extracted:
                self.subscribed_shows.add(subscribed_show)


    class Meta:
        model = User


class ShowFactory(factory.DjangoModelFactory):
    name = factory.Faker('word')
    url = factory.Faker('url')

    class Meta:
        model = Show


@factory.django.mute_signals(signals.post_save)
class PerformanceFactory(factory.DjangoModelFactory):
    show = factory.SubFactory(ShowFactory)
    starts_at = factory.Faker('date_time', tzinfo=pytz.utc)

    class Meta:
        model = Performance


class LotteryFactory(factory.DjangoModelFactory):
    performance = factory.SubFactory(PerformanceFactory)
    external_performance_id = factory.Faker('pyint')
    nonce = factory.Faker('pystr')
    starts_at = factory.Faker('date_time', tzinfo=pytz.utc)
    ends_at = factory.Faker('date_time', tzinfo=pytz.utc)
    entered_users = factory.RelatedFactory(UserFactory)

    class Meta:
        model = Lottery

    @factory.post_generation
    def entered_users(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            print(extracted)
            for entered_user in extracted:
                self.entered_users.add(entered_user)