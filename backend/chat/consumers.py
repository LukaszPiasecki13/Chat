import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data['message']
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']
        print(f"Received message from {sender_id} to {receiver_id}: {message_text}")

        from django.contrib.auth.models import User
        sender_user = await database_sync_to_async(User.objects.get)(id=sender_id)

        # Check permissions
        from .permissions import can_send_message
        allowed, reason = await can_send_message(sender_user, receiver_id)
        if not allowed:
            await self.send(text_data=json.dumps({"error": reason}))
            return

        message = await self.save_message(sender_id, receiver_id, message_text)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'timestamp': str(message.timestamp),
            }
        )


    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, content):
        from .models import Message
        from django.contrib.auth.models import User
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        return Message.objects.create(sender=sender, receiver=receiver, content=content)

