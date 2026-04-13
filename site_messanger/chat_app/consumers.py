from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'test_group'
        # await self.channel_layer.group_add(self.room_group_name, self.channel_name) - 
        # Додає користувача у WS групу, щоб об'єднати декілька користувачів ( self.room_group_name - потрібно створити )
        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name
        )
        await self.accept()
        await self.send(json.dumps({
            'message': 'Server connect'
        }))
    async def receive(self, text_data: str):
        data = json.loads(text_data)
        #  await self.channel_layer.group_send(self.room_group_name, {
        #   "type": "chat_send" - назва функції
        # }) - Відправляє повідомлення всім користувачам групи ( викликаючи у кожного з них вказану функцію )
        # Відправляти повідомлення потрібно в функції chat_send( приймає параметр event )
        await self.channel_layer.group_send(
            self.room_group_name,
            {   
                "type": "chat_send",
                "message": data.get("message")
            } 
        )
    async def chat_send(self, event):
        await self.send(json.dumps(event))