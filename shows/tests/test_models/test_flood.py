import pytest
from datetime import timedelta
from ...factories import FloodFactory, UserFactory, SESFactory, LotteryFactory


@pytest.mark.django_db
def test_generated_users():
    client = UserFactory()
    lottery = LotteryFactory()
    ses0 = SESFactory(user=client)
    ses1 = SESFactory(user=client)
    ses2 = SESFactory(user=client)
    flood = FloodFactory(client=client, manager=client, lottery=lottery)
    generated_users = list(flood.generate_users())

    assert generated_users[0].email == ses0.email
    assert generated_users[0].date_of_birth == client.date_of_birth

    assert generated_users[1].email == ses1.email
    assert generated_users[1].date_of_birth == client.date_of_birth + timedelta(days=1)

    assert generated_users[2].email == ses2.email
    assert generated_users[2].date_of_birth == client.date_of_birth + timedelta(days=2)


