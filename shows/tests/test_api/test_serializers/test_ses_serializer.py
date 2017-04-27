from ....api.serializers import SESSerializer
from ....factories import SESFactory, UserFactory


def test_it():
    user = UserFactory.build()
    ses = SESFactory.build(user=user)
    serializer = SESSerializer(ses)
    assert serializer.data['email'] == ses.email
    assert serializer.data['id'] is None
    assert serializer.data['user']['email'] == user.email
