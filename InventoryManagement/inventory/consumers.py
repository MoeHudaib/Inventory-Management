import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.group_name = f'user_{self.user.id}_orders'
        
        # Join the WebSocket group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the WebSocket group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Here you could handle incoming WebSocket messages if needed
        pass

    # Receive message from the WebSocket group
    async def send_order_update(self, event):
        message = event['message']
        
        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
