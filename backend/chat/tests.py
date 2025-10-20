import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from channels.testing import WebsocketCommunicator

from .models import Profile, Contact, Message
from .serializers import UserSerializer, MessageSerializer
from .permissions import can_send_message
from .consumers import ChatConsumer


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_factory(db):
    def create_user(username, role=None):
        user = User.objects.create_user(username=username, password='testpass123')
        if role:
            Profile.objects.create(user=user, role=role)
        return user
    return create_user

@pytest.fixture
def player_user(user_factory):
    return user_factory('player1', role=Profile.Role.PLAYER)

@pytest.fixture
def official_user(user_factory):
    return user_factory('official1', role=Profile.Role.OFFICIAL)

@pytest.fixture
def another_player(user_factory):
    return user_factory('player2', role=Profile.Role.PLAYER)

@pytest.fixture
def another_official(user_factory):
    return user_factory('official2', role=Profile.Role.OFFICIAL)


@pytest.mark.django_db
def test_create_player_profile(player_user):
    profile = player_user.profile
    assert profile.user == player_user
    assert profile.role == Profile.Role.PLAYER
    assert str(profile) == f"{player_user.username} (player)"

@pytest.mark.django_db
def test_create_official_profile(official_user):
    profile = official_user.profile
    assert profile.role == Profile.Role.OFFICIAL
    assert str(profile) == f"{official_user.username} (official)"

@pytest.mark.django_db
def test_unique_contact_constraint(player_user, official_user):
    Contact.objects.create(user1=player_user, user2=official_user)
    with pytest.raises(IntegrityError):
        Contact.objects.create(user1=player_user, user2=official_user)

@pytest.mark.django_db
def test_message_creation_and_ordering(player_user, official_user):
    msg1 = Message.objects.create(sender=player_user, receiver=official_user, content="First message")
    msg2 = Message.objects.create(sender=official_user, receiver=player_user, content="Second message")
    assert msg1.content == "First message"
    assert str(msg1) == f"From {player_user.username} to {official_user.username} at {msg1.timestamp}"
    messages = list(Message.objects.all())
    assert messages == [msg1, msg2]

@pytest.mark.django_db
def test_user_serializer_with_profile(player_user):
    serializer = UserSerializer(player_user)
    data = serializer.data
    assert data['id'] == player_user.id
    assert data['username'] == player_user.username
    assert data['profile']['role'] == Profile.Role.PLAYER

@pytest.mark.django_db
def test_user_serializer_without_profile(user_factory):
    user_no_profile = user_factory('no_profile_user')
    serializer = UserSerializer(user_no_profile)
    assert serializer.data['profile'] is None

@pytest.mark.django_db
def test_message_serializer_deserialization(player_user, official_user):
    valid_data = {'receiver_id': official_user.id, 'content': 'Valid message'}
    serializer = MessageSerializer(data=valid_data, context={'sender': player_user})
    assert serializer.is_valid(raise_exception=True)

    invalid_data = {'receiver_id': 999, 'content': 'Invalid message'}
    serializer = MessageSerializer(data=invalid_data, context={'sender': player_user})
    assert not serializer.is_valid()
    assert 'receiver_id' in serializer.errors

@pytest.mark.django_db
def test_user_list_view(api_client, player_user, official_user, another_player):
    api_client.force_authenticate(user=player_user)
    response = api_client.get(reverse('user-list'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    usernames = {user['username'] for user in response.data}
    assert usernames == {official_user.username, another_player.username}

@pytest.mark.django_db
def test_conversation_list_view(api_client, player_user, official_user):
    Message.objects.create(sender=player_user, receiver=official_user, content="Hello")
    Message.objects.create(sender=official_user, receiver=player_user, content="Hi back")

    api_client.force_authenticate(user=player_user)
    url = reverse('conversation-list', kwargs={'user_id': official_user.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]['content'] == "Hello"
    assert response.data[1]['content'] == "Hi back"


@pytest.mark.django_db(transaction=True)
async def test_official_cannot_contact_official(official_user, another_official):
    allowed, reason = await can_send_message(official_user, another_official.id)
    assert not allowed
    assert reason == "Officials cannot contact each other."

@pytest.mark.django_db(transaction=True)
async def test_player_daily_limit_to_official(player_user, official_user):
    for i in range(5):
        await Message.objects.acreate(sender=player_user, receiver=official_user, content=f"Msg {i+1}")
    allowed, reason = await can_send_message(player_user, official_user.id)
    assert not allowed
    assert "daily limit of 5 messages" in reason


@pytest.mark.django_db(transaction=True)
async def test_player_total_daily_limit(player_user, official_user, another_player):

    for i in range(95):
        await Message.objects.acreate(sender=player_user, receiver=another_player, content=f"Msg to player {i+1}")

    for i in range(5):
        await Message.objects.acreate(sender=player_user, receiver=official_user, content=f"Msg to official {i+1}")
    

    allowed, reason = await can_send_message(player_user, another_player.id)
    assert not allowed

    assert "You have reached your daily limit of 100 messages." in reason

