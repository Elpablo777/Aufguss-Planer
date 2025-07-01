import json
import jwt
import urllib.parse as urlparse
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import AnonymousUser, User
from .models import SaunaUser, ChatMessage

class AufgussConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = await self.get_user_from_token()
        if not self.user or not self.user.is_authenticated:
            await self.close()
            return
        await self.channel_layer.group_add("aufguss_updates", self.channel_name)
        await self.accept()
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("aufguss_updates", self.channel_name)
    async def aufguss_update(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'aufguss': event['aufguss']
        }))

    @database_sync_to_async
    def get_user_from_token(self):
        # Versuche, den Token aus den Subprotokollen zu lesen
        token = None
        if self.scope.get('subprotocols'):
            # Der Token sollte das einzige Subprotokoll sein
            token = self.scope['subprotocols'][0]

        if not token:
            # Fallback: Versuche, den Token aus dem Query-String zu lesen (für Abwärtskompatibilität oder andere Clients)
            query_string = self.scope.get('query_string', b'').decode()
            params = dict(qp.split('=') for qp in query_string.split('&') if '=' in qp)
            token = params.get('token')

        if not token:
            return AnonymousUser()
        try:
            UntypedToken(token)  # prüft Gültigkeit
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('user_id')
            return User.objects.get(id=user_id)
        except (InvalidToken, TokenError, User.DoesNotExist, Exception):
            return AnonymousUser()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = await self.get_user_from_token() # Dieselbe Logik für ChatConsumer verwenden
        if not self.user or not self.user.is_authenticated:
            await self.close()
            return
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat", self.channel_name)
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user_id = data['user_id']
        await self.save_message(user_id, message)
        await self.channel_layer.group_send(
            "chat",
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id,
                'username': await self.get_username(user_id),
                'timestamp': self.get_timestamp()
            }
        )
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
    @database_sync_to_async
    def save_message(self, user_id, message):
        user = SaunaUser.objects.get(id=user_id)
        ChatMessage.objects.create(sender=user, content=message)
    @database_sync_to_async
    def get_username(self, user_id):
        user = SaunaUser.objects.get(id=user_id)
        return user.full_name
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%d.%m.%Y, %H:%M:%S")
    # Die get_user_from_token Methode ist jetzt im AufgussConsumer und wird hier nicht erneut definiert,
    # stattdessen sollte eine gemeinsame Basisklasse oder ein Utility verwendet werden.
    # Für diese Änderung gehe ich davon aus, dass der ChatConsumer die Logik des AufgussConsumer nutzt
    # oder wir passen sie hier identisch an. Um Redundanz zu vermeiden, sollte die Methode
    # zentralisiert werden. Da sie aber schon im AufgussConsumer existiert und modifiziert wurde,
    # und ChatConsumer eine eigene Definition hatte, passe ich diese hier ebenfalls an.

    @database_sync_to_async
    def get_user_from_token(self):
        # Versuche, den Token aus den Subprotokollen zu lesen
        token = None
        if self.scope.get('subprotocols'):
            # Der Token sollte das einzige Subprotokoll sein
            token = self.scope['subprotocols'][0]

        if not token:
            # Fallback: Versuche, den Token aus dem Query-String zu lesen
            query_string = self.scope.get('query_string', b'').decode()
            params = urlparse.parse_qs(query_string)
            token_list = params.get('token', [])
            if token_list:
                token = token_list[0]

        if not token:
            return AnonymousUser()
        try:
            UntypedToken(token)  # prüft Gültigkeit
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('user_id')
            return User.objects.get(id=user_id)
        except (InvalidToken, TokenError, User.DoesNotExist, Exception):
            return AnonymousUser()
