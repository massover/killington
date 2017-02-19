import factory
import pytz

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

    class Meta:
        model = User


class ShowFactory(factory.DjangoModelFactory):
    name = factory.Faker('word')
    url = factory.Faker('url')
    subscribed_users = factory.RelatedFactory(UserFactory)

    class Meta:
        model = Show

    @factory.post_generation
    def subscribed_users(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for subscribed_user in extracted:
                self.subscribed_users.add(subscribed_user)


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
    processed = factory.Faker('pybool')

    class Meta:
        model = Lottery