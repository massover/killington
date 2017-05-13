from ....api.serializers import UserSerializer
from ....factories import UserFactory


def test_it():
    user = UserFactory.build()
    serializer = UserSerializer(user)
    assert serializer.data['email'] == user.email
    assert serializer.data['id'] is None
