from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        """
        Called when a client opens a WebSocket connection.
        """
        await self.accept()

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes.
        """
        pass

    async def receive_json(self, content, **kwargs):
        """
        Called when the client sends JSON.
        """
        pass