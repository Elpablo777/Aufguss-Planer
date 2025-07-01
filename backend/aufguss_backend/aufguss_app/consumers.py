import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import SaunaUser, ChatMessage

class AufgussConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("aufguss_updates", self.channel_name)
        await self.accept()
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("aufguss_updates", self.channel_name)
    async def aufguss_update(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'aufguss': event['aufguss']
        }))

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
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
