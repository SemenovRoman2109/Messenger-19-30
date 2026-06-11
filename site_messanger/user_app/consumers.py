from channels.generic.websocket import AsyncWebsocketConsumer
import json

online_users = {}

class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user')
        self.room_group_name = 'presence'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        self.user_group_name = f'user_{self.user.id}'
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        await self.accept()
        if self.user.id in online_users:
            online_users[self.user.id] += 1
        else:
            online_users[self.user.id] = 1
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': "send_status",
                    'status': True,
                    'user_id': self.user.id
                }
            )

        await self.send(json.dumps({
            'type': 'get_online',
            'online_users': online_users,
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name, 
            self.channel_name
        )
        await self.channel_layer.group_discard(
            self.user_group_name, 
            self.channel_name
        )
        
        online_users[self.user.id] -= 1
        if online_users[self.user.id] <= 0:
            del online_users[self.user.id]
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': "send_status",
                    'status': False,
                    'user_id': self.user.id
                }
            )


    async def receive(self, text_data):
        await self.send(json.dumps({
            'type': 'get_online',
            'online_users': online_users,
        }))


    async def send_status(self, data):
        await self.send(text_data= json.dumps(data))

    async def send_message(self, data):
        await self.send(text_data= json.dumps(data))