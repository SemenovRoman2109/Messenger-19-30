from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import *

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope.get("url_route").get("kwargs").get("chat_id")
        self.room_group_name = f"chat_{self.chat_id}"
        has_access = await self.user_has_access()
        if has_access:
            await self.channel_layer.group_add(
                self.room_group_name, 
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()
            
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name, 
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data.get("msg")
        if text.strip():
            message = await self.save_message(text)
            for member_id in message['members_id']:
                await self.channel_layer.group_send(
                    f"user_{member_id}",
                    {
                        'type': 'send_message',
                        'chat_id': self.chat_id,
                    }
                )
            await self.channel_layer.group_send(
                self.room_group_name, 
                {
                    "type": "send_message",
                    "message": message,
                }
            )
            
    @database_sync_to_async
    def user_has_access(self):
        user = self.scope.get("user")
        if user.is_authenticated:
            chat = Chat.objects.filter(id = self.chat_id, users = user)
            return chat.exists()
        return False
    
    @database_sync_to_async
    def save_message(self, text):
        user = self.scope.get("user")
        new_message = Message.objects.create(text = text, chat_id=self.chat_id, sender=user)
        members_id = []
        for user in new_message.chat.users.all():
            members_id.append(user.id)
        return {
            'sender': new_message.sender.email,
            'text': new_message.text,
            'date': str(new_message.created_at.date()),
            'time': str(new_message.created_at.timetuple().tm_hour) + ":" + str(new_message.created_at.timetuple().tm_min),
            'images': [],
            "id": new_message.id,
            'members_id': members_id
        }
            # "sender_image_url": new_message.sender.avatar.url
            
    @database_sync_to_async   
    def read_message(self, message_id):
        user = self.scope.get("user")
        message = Message.objects.filter(id= message_id).first()
        if user != message.sender:
            message.readers.add(user)


    async def send_message(self, data):
        await self.read_message(message_id= data["message"]["id"])
        await self.send(text_data= json.dumps(data))