import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from aufguss_app.models import SaunaUser, AufgussSession, ChatMessage # ChatMessage hinzugefügt
from aufguss_app.consumers import AufgussConsumer, ChatConsumer # Consumer hinzugefügt
import datetime
import json # json Import hinzugefügt
from channels.testing import WebsocketCommunicator # WebsocketCommunicator hinzugefügt
from channels.layers import get_channel_layer # Channel Layer für Tests
from rest_framework_simplejwt.tokens import AccessToken # Für Token-Generierung in Tests

# Hilfsfunktion zum Erstellen eines gültigen Tokens für einen Benutzer
def get_token_for_user(user):
    access = AccessToken.for_user(user)
    return str(access)

@pytest.mark.django_db
def test_user_login_and_jwt():
    user = User.objects.create_user(username='testuser', password='testpass')
    SaunaUser.objects.create(user=user, full_name='Test User')
    client = APIClient()
    response = client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    assert 'access' in response.data

@pytest.mark.django_db
def test_aufguss_crud():
    user = User.objects.create_user(username='testuser2', password='testpass')
    sauna_user = SaunaUser.objects.create(user=user, full_name='Test User2')
    client = APIClient()
    token = client.post(reverse('token_obtain_pair'), {'username': 'testuser2', 'password': 'testpass'}).data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    # Create
    data = {
        'title': 'Test Aufguss',
        'description': 'Test Desc',
        'start_time': datetime.datetime.now().isoformat(),
        'end_time': (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat(),
        'created_by': sauna_user.id
    }
    response = client.post('/api/aufguesse/', data, format='json')
    assert response.status_code == 201
    aufguss_id = response.data['id']
    # Read
    response = client.get(f'/api/aufguesse/{aufguss_id}/')
    assert response.status_code == 200
    # Update
    response = client.put(f'/api/aufguesse/{aufguss_id}/', {**data, 'title': 'Updated'}, format='json')
    assert response.status_code == 200
    # Delete
    response = client.delete(f'/api/aufguesse/{aufguss_id}/')
    assert response.status_code == 204

@pytest.mark.django_db
def test_user_viewset_permissions_and_me_action():
    # Create admin user
    admin_user = User.objects.create_user(username='admin', password='testpass', is_staff=True)
    SaunaUser.objects.create(user=admin_user, full_name='Admin User')

    # Create normal user
    normal_user = User.objects.create_user(username='normaluser', password='testpass')
    sauna_user_normal = SaunaUser.objects.create(user=normal_user, full_name='Normal User')

    client = APIClient()

    # Test 'me' action for normal user
    token_normal = client.post(reverse('token_obtain_pair'), {'username': 'normaluser', 'password': 'testpass'}).data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_normal)
    response_me = client.get(reverse('saunauser-me')) # 'saunauser-me' ist der basename + action
    assert response_me.status_code == 200
    assert response_me.data['full_name'] == 'Normal User'

    # Test list action (safe method) for normal user - should be allowed
    response_list_normal = client.get(reverse('saunauser-list'))
    assert response_list_normal.status_code == 200

    # Test create action (unsafe method) for normal user - should be forbidden
    user_data = {'user': normal_user.id, 'full_name': 'Attempted Create', 'color': '#123456'}
    response_create_normal = client.post(reverse('saunauser-list'), user_data, format='json')
    assert response_create_normal.status_code == 403 # Forbidden

    # Test retrieve action for another user by normal user (safe method) - should be allowed
    response_retrieve_other_normal = client.get(reverse('saunauser-detail', args=[sauna_user_normal.id]))
    assert response_retrieve_other_normal.status_code == 200

    # Test update action for another user by normal user (unsafe method) - should be forbidden
    response_update_other_normal = client.patch(reverse('saunauser-detail', args=[sauna_user_normal.id]), {'full_name': 'Updated Name'}, format='json')
    assert response_update_other_normal.status_code == 403

    # Test 'me' action for admin user
    client.credentials() # Clear previous credentials
    token_admin = client.post(reverse('token_obtain_pair'), {'username': 'admin', 'password': 'testpass'}).data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_admin)
    response_me_admin = client.get(reverse('saunauser-me'))
    assert response_me_admin.status_code == 200
    assert response_me_admin.data['full_name'] == 'Admin User'

    # Test create action for admin user - should be allowed
    # We need to create a new underlying Django user first for the SaunaUser
    new_django_user = User.objects.create_user(username='newdjango', password='testpassword')
    admin_create_data = {'user': new_django_user.id, 'full_name': 'Created by Admin', 'color': '#ABCDEF'}
    response_create_admin = client.post(reverse('saunauser-list'), admin_create_data, format='json')
    assert response_create_admin.status_code == 201
    created_sauna_user_id = response_create_admin.data['id']

    # Test update action for another user by admin user - should be allowed
    response_update_other_admin = client.patch(reverse('saunauser-detail', args=[created_sauna_user_id]), {'full_name': 'Admin Was Here'}, format='json')
    assert response_update_other_admin.status_code == 200
    assert response_update_other_admin.data['full_name'] == 'Admin Was Here'

    # Test delete action by admin user - should be allowed
    response_delete_admin = client.delete(reverse('saunauser-detail', args=[created_sauna_user_id]))
    assert response_delete_admin.status_code == 204


@pytest.mark.django_db
class TestAufgussViewSet:
    """Tests for the AufgussViewSet API endpoints and functionality."""
    @pytest.fixture
    def setup_users_and_client(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='testpass1')
        self.sauna_user1 = SaunaUser.objects.create(user=self.user1, full_name='User Eins', color='#FF0000')

        self.user2 = User.objects.create_user(username='user2', password='testpass2')
        self.sauna_user2 = SaunaUser.objects.create(user=self.user2, full_name='User Zwei', color='#00FF00')

        # Authenticate client as user1
        token = self.client.post(reverse('token_obtain_pair'), {'username': 'user1', 'password': 'testpass1'}).data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        return self.client, self.sauna_user1, self.sauna_user2

    def test_my_sessions_action(self, setup_users_and_client):
        client, sauna_user1, sauna_user2 = setup_users_and_client

        # Aufguss for user1
        AufgussSession.objects.create(
            title='User1 Aufguss', start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now() + datetime.timedelta(hours=1), created_by=sauna_user1
        )
        # Aufguss for user2
        AufgussSession.objects.create(
            title='User2 Aufguss', start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now() + datetime.timedelta(hours=1), created_by=sauna_user2
        )

        response = client.get(reverse('aufgusssession-my-sessions')) # Basename 'aufgusssession'
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['title'] == 'User1 Aufguss'

    def test_aufguss_creation_validation_errors(self, setup_users_and_client):
        client, sauna_user1, _ = setup_users_and_client

        # Missing title
        data_missing_title = {
            'description': 'Test Desc',
            'start_time': datetime.datetime.now().isoformat(),
            'end_time': (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat(),
            'created_by': sauna_user1.id
        }
        response = client.post(reverse('aufgusssession-list'), data_missing_title, format='json')
        assert response.status_code == 400
        assert 'title' in response.data

        # Start time after end time
        data_invalid_time = {
            'title': 'Invalid Time Aufguss',
            'start_time': (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat(),
            'end_time': datetime.datetime.now().isoformat(),
            'created_by': sauna_user1.id
        }
        # Annahme: Serializer oder Modell hat eine Validierung dafür.
        # Wenn nicht, muss diese erst implementiert werden.
        # Fürs Erste prüfen wir, ob der Serializer dies abfängt, wenn er `validate` überschreibt.
        # Standardmäßig wird dies nicht vom ModelSerializer geprüft, es sei denn, man fügt validate hinzu.
        # Ich gehe davon aus, dass eine solche Validierung fehlt und der Test fehlschlagen würde oder 201 zurückgibt.
        # Um den Test erfolgreich zu machen, müsste die Validierung im AufgussSerializer hinzugefügt werden.
        # Diese wurde nun im AufgussSerializer implementiert.
        response_invalid_time = client.post(reverse('aufgusssession-list'), data_invalid_time, format='json')
        assert response_invalid_time.status_code == 400
        assert 'end_time' in response_invalid_time.data # Der Fehler wird auf 'end_time' bezogen
        assert response_invalid_time.data['end_time'][0] == "Endzeit muss nach der Startzeit liegen."


    def test_aufguss_permissions_update_delete_others_aufguss(self, setup_users_and_client):
        client, sauna_user1, sauna_user2 = setup_users_and_client

        # Aufguss created by user2
        aufguss_user2 = AufgussSession.objects.create(
            title='User2 Aufguss Original', start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now() + datetime.timedelta(hours=1), created_by=sauna_user2
        )

        # User1 (authenticated client) tries to update Aufguss from User2
        update_data = {'title': 'User1 tried to change this'}
        response_update = client.put(
            reverse('aufgusssession-detail', args=[aufguss_user2.id]),
            {**AufgussSerializer(aufguss_user2).data, **update_data}, # Sende volle Daten für PUT
            format='json'
        )
        # Standard ModelViewSet permissions (IsAuthenticated) allow any authenticated user to update/delete any object.
        # This needs to be restricted if only owners or admins should modify.
        # Aktuell sollte dieser Test fehlschlagen (200 OK), wenn keine spezifischen Objekt-Level-Berechtigungen implementiert sind.
        # Ich füge eine Annahme hinzu, dass dies fehlschlagen soll (403/404) und markiere es als TODO.
        # TODO: Implement object-level permissions for AufgussViewSet (e.g., owner can edit/delete, or admin).
        assert response_update.status_code in [403, 404] # Expecting Forbidden or Not Found if not owner

        # User1 (authenticated client) tries to delete Aufguss from User2
        response_delete = client.delete(reverse('aufgusssession-detail', args=[aufguss_user2.id]))
        assert response_delete.status_code in [403, 404] # Now expecting 403 due to IsOwnerOrAdminOrReadOnly
        assert AufgussSession.objects.filter(id=aufguss_user2.id).exists() # Should still exist


@pytest.mark.django_db
class TestChatViewSet:
    """Tests for the ChatMessageViewSet API endpoints and functionality."""
    @pytest.fixture
    def setup_users_and_client(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='chatuser1', password='testpass1')
        self.sauna_user1 = SaunaUser.objects.create(user=self.user1, full_name='Chat User Eins')

        self.user2 = User.objects.create_user(username='chatuser2', password='testpass2')
        self.sauna_user2 = SaunaUser.objects.create(user=self.user2, full_name='Chat User Zwei')

        self.admin_user = User.objects.create_user(username='chatadmin', password='testpassadmin', is_staff=True)
        self.sauna_admin_user = SaunaUser.objects.create(user=self.admin_user, full_name='Chat Admin')

        # Authenticate client as user1 by default
        token = self.client.post(reverse('token_obtain_pair'), {'username': 'chatuser1', 'password': 'testpass1'}).data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        return self.client, self.sauna_user1, self.sauna_user2, self.sauna_admin_user

    def test_create_and_list_chat_messages(self, setup_users_and_client):
        client, sauna_user1, _, _ = setup_users_and_client

        # Create message as user1
        message_data = {'content': 'Hallo Welt von User1!'}
        response_create = client.post(reverse('chatmessage-list'), message_data, format='json')
        assert response_create.status_code == 201
        assert response_create.data['content'] == 'Hallo Welt von User1!'
        assert response_create.data['sender_name'] == sauna_user1.full_name
        message_id = response_create.data['id']

        # List messages
        response_list = client.get(reverse('chatmessage-list'))
        assert response_list.status_code == 200
        assert len(response_list.data) > 0
        assert any(msg['id'] == message_id for msg in response_list.data)

    def test_chat_message_unrestricted_update_delete_initially(self, setup_users_and_client):
        client, sauna_user1, sauna_user2, _ = setup_users_and_client

        # Message created by user2
        msg_by_user2 = ChatMessage.objects.create(sender=sauna_user2, content="User2's message")

        # User1 (authenticated client) tries to update message from User2
        update_data = {'content': "User1 updated User2's message"}
        # For PUT, all required fields must be provided or they will be set to blank/null if allowed
        # The serializer for ChatMessage has 'sender' as a writeable field (though it's ignored by perform_create)
        # To avoid issues with PUT, we can use PATCH or ensure all fields are there.
        # Let's use PATCH for partial update.
        response_update = client.patch(reverse('chatmessage-detail', args=[msg_by_user2.id]), update_data, format='json')

        # Initially, without specific object-level permissions, this would be allowed (200 OK)
        # This assertion is expected to FAIL until permissions are implemented.
        # For now, we comment it out and will enable it after adding permissions.
        # assert response_update.status_code == 200
        # assert ChatMessage.objects.get(id=msg_by_user2.id).content == "User1 updated User2's message"

        # User1 tries to delete message from User2
        response_delete = client.delete(reverse('chatmessage-detail', args=[msg_by_user2.id]))
        # Initially, this would also be allowed (204 No Content)
        # This assertion is expected to FAIL until permissions are implemented.
        # assert response_delete.status_code == 204
        # assert not ChatMessage.objects.filter(id=msg_by_user2.id).exists()

        # We add a placeholder assertion to make the test runnable for now.
        # This will be removed once the permission logic is in place and the above asserts are active.
        # User1 (authenticated client) tries to update message from User2 - should be forbidden
        assert response_update.status_code == 403
        db_msg_content = ChatMessage.objects.get(id=msg_by_user2.id).content
        assert db_msg_content == "User2's message" # Content should not have changed

        # User1 tries to delete message from User2 - should be forbidden
        assert response_delete.status_code == 403
        assert ChatMessage.objects.filter(id=msg_by_user2.id).exists() # Should still exist

    def test_chat_message_owner_can_update_delete(self, setup_users_and_client):
        client, sauna_user1, _, _ = setup_users_and_client

        # Message created by user1
        msg_by_user1 = ChatMessage.objects.create(sender=sauna_user1, content="User1's original message")

        # User1 updates their own message
        update_data = {'content': "User1's updated message"}
        response_update = client.patch(reverse('chatmessage-detail', args=[msg_by_user1.id]), update_data, format='json')
        assert response_update.status_code == 200
        assert ChatMessage.objects.get(id=msg_by_user1.id).content == "User1's updated message"

        # User1 deletes their own message
        response_delete = client.delete(reverse('chatmessage-detail', args=[msg_by_user1.id]))
        assert response_delete.status_code == 204
        assert not ChatMessage.objects.filter(id=msg_by_user1.id).exists()

    def test_chat_message_admin_can_update_delete_others_message(self, setup_users_and_client):
        client, _, sauna_user2, sauna_admin_user = setup_users_and_client

        # Message created by user2
        msg_by_user2 = ChatMessage.objects.create(sender=sauna_user2, content="User2's message for admin test")

        # Authenticate as admin
        admin_token = client.post(reverse('token_obtain_pair'), {'username': 'chatadmin', 'password': 'testpassadmin'}).data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_token)

        # Admin updates User2's message
        update_data = {'content': "Admin updated User2's message"}
        response_update = client.patch(reverse('chatmessage-detail', args=[msg_by_user2.id]), update_data, format='json')
        assert response_update.status_code == 200
        assert ChatMessage.objects.get(id=msg_by_user2.id).content == "Admin updated User2's message"

        # Admin deletes User2's message
        # Create another message to delete, to ensure the previous one is gone
        msg_to_delete_by_admin = ChatMessage.objects.create(sender=sauna_user2, content="Another one for admin")
        response_delete = client.delete(reverse('chatmessage-detail', args=[msg_to_delete_by_admin.id]))
        assert response_delete.status_code == 204
        assert not ChatMessage.objects.filter(id=msg_to_delete_by_admin.id).exists()


@pytest.mark.django_db
@pytest.mark.asyncio # Mark test class as asyncio
class TestAufgussConsumer:
    """Tests for the AufgussConsumer WebSocket functionality."""
    @pytest.fixture
    async def setup_user(self): # Make fixture async
        user = await database_sync_to_async(User.objects.create_user)(username='ws_user', password='testpassword')
        await database_sync_to_async(SaunaUser.objects.create)(user=user, full_name='WebSocket User')
        return user

    async def test_aufguss_consumer_connect_valid_token(self, setup_user):
        user = await setup_user # await the fixture
        token = await database_sync_to_async(get_token_for_user)(user)

        communicator = WebsocketCommunicator(AufgussConsumer.as_asgi(), f"/ws/aufguss/?token={token}")
        # Alternative: Senden des Tokens im Subprotokoll
        # communicator = WebsocketCommunicator(AufgussConsumer.as_asgi(), "/ws/aufguss/", subprotocols=[token])

        connected, subprotocol = await communicator.connect()
        assert connected
        await communicator.disconnect()

    async def test_aufguss_consumer_connect_invalid_token(self):
        communicator = WebsocketCommunicator(AufgussConsumer.as_asgi(), "/ws/aufguss/?token=invalidtoken")
        connected, subprotocol = await communicator.connect()
        assert not connected # Verbindung sollte fehlschlagen oder geschlossen werden
        # Optional: await communicator.disconnect() - kann einen Fehler werfen, wenn die Verbindung nie richtig hergestellt wurde.

    async def test_aufguss_consumer_connect_no_token(self):
        communicator = WebsocketCommunicator(AufgussConsumer.as_asgi(), "/ws/aufguss/")
        connected, subprotocol = await communicator.connect()
        assert not connected

    async def test_aufguss_consumer_receives_group_message(self, setup_user):
        user = await setup_user
        token = await database_sync_to_async(get_token_for_user)(user)

        communicator = WebsocketCommunicator(AufgussConsumer.as_asgi(), f"/ws/aufguss/?token={token}")
        # communicator = WebsocketCommunicator(AufgussConsumer.as_asgi(), "/ws/aufguss/", subprotocols=[token])
        connected, _ = await communicator.connect()
        assert connected

        channel_layer = get_channel_layer()
        test_aufguss_data = {"id": "test-uuid", "title": "Test Event"}
        await channel_layer.group_send(
            "aufguss_updates",
            {
                "type": "aufguss.update", # Beachte den Punkt statt Unterstrich für den Handler-Namen
                "aufguss": test_aufguss_data,
            },
        )

        response = await communicator.receive_from()
        data = json.loads(response)

        assert data['type'] == 'aufguss_update' # Der Consumer sendet 'aufguss_update'
        assert data['aufguss']['title'] == "Test Event"

        await communicator.disconnect()

    # Wichtiger Hinweis: In consumers.py ist der Handler `async def aufguss_update(self, event):`
    # Der Typ im group_send sollte daher eher `aufguss.update` sein, damit Channels die Methode korrekt findet.
    # Der Consumer selbst sendet dann eine Nachricht mit `type: 'aufguss_update'`.
    # Ich habe das im Test oben angepasst (`"type": "aufguss.update"`).


@pytest.mark.django_db
@pytest.mark.asyncio
class TestChatConsumer:
    """Tests for the ChatConsumer WebSocket functionality."""
    @pytest.fixture
    async def setup_user_chat(self): # Eindeutiger Name für die Fixture
        user = await database_sync_to_async(User.objects.create_user)(username='ws_chat_user', password='testpassword')
        sauna_user = await database_sync_to_async(SaunaUser.objects.create)(user=user, full_name='WebSocket Chat User')
        return user, sauna_user

    async def test_chat_consumer_connect_valid_token(self, setup_user_chat):
        user, _ = await setup_user_chat
        token = await database_sync_to_async(get_token_for_user)(user)

        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), f"/ws/chat/?token={token}")
        # communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chat/", subprotocols=[token])
        connected, _ = await communicator.connect()
        assert connected
        await communicator.disconnect()

    async def test_chat_consumer_connect_invalid_token(self):
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chat/?token=invalidtoken")
        connected, _ = await communicator.connect()
        assert not connected

    async def test_chat_consumer_send_receive_message(self, setup_user_chat):
        user, sauna_user = await setup_user_chat
        token = await database_sync_to_async(get_token_for_user)(user)

        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), f"/ws/chat/?token={token}")
        # communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chat/", subprotocols=[token])
        connected, _ = await communicator.connect()
        assert connected

        message_to_send = {"message": "Hello from test!", "user_id": sauna_user.id}
        await communicator.send_to(text_data=json.dumps(message_to_send))

        # Der Consumer sendet die Nachricht an die Gruppe, und die Gruppe sendet sie an alle Clients (auch den Sender).
        response = await communicator.receive_from()
        data = json.loads(response)

        assert data['type'] == 'chat_message'
        assert data['message'] == "Hello from test!"
        assert data['user_id'] == sauna_user.id
        assert data['username'] == sauna_user.full_name

        # Überprüfen, ob die Nachricht in der DB gespeichert wurde
        message_exists = await database_sync_to_async(ChatMessage.objects.filter(sender=sauna_user, content="Hello from test!").exists)()
        assert message_exists

        await communicator.disconnect()

    async def test_chat_consumer_receives_message_from_other_client_via_group(self, setup_user_chat):
        user1, sauna_user1 = await setup_user_chat # client1
        user2 = await database_sync_to_async(User.objects.create_user)(username='ws_chat_user2', password='testpassword2')
        sauna_user2 = await database_sync_to_async(SaunaUser.objects.create)(user=user2, full_name='WebSocket Chat User Zwei')

        token1 = await database_sync_to_async(get_token_for_user)(user1)
        # token2 = await database_sync_to_async(get_token_for_user)(user2) # Nicht benötigt für diesen Testablauf

        comm1 = WebsocketCommunicator(ChatConsumer.as_asgi(), f"/ws/chat/?token={token1}")
        await comm1.connect()

        comm2 = WebsocketCommunicator(ChatConsumer.as_asgi(), f"/ws/chat/?token={token1}") # Simuliert anderen Client, aber mit demselben Token für Einfachheit des Tests
        await comm2.connect()


        # Nachricht wird direkt an den Channel Layer gesendet, als käme sie von einem anderen Consumer-Aufruf
        # (z.B. simuliert durch den receive-Handler eines anderen Clients)
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            "chat",  # Gruppenname
            {
                "type": "chat.message",  # Handler-Name: chat_message
                "message": "Broadcast test",
                "user_id": sauna_user2.id,  # Simuliert Nachricht von user2
                "username": sauna_user2.full_name,
                "timestamp": datetime.datetime.now().strftime(
                    "%d.%m.%Y, %H:%M:%S"
                )
            }
        )

        # Client1 sollte die Nachricht empfangen
        response1 = await comm1.receive_from()
        data1 = json.loads(response1)
        assert data1['message'] == "Broadcast test"
        assert data1['user_id'] == sauna_user2.id

        # Client2 sollte die Nachricht ebenfalls empfangen
        response2 = await comm2.receive_from()
        data2 = json.loads(response2)
        assert data2['message'] == "Broadcast test"
        assert data2['user_id'] == sauna_user2.id

        await comm1.disconnect()
        await comm2.disconnect()
