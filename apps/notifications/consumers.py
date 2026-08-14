from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        user = self.scope["user"]

        print("WebSocket user:", user)

        if user.is_anonymous:
            print("WebSocket rejected: AnonymousUser")
            await self.close()
            return

        self.user_group_name = f"user_{user.id}"

        print("Joining group:", self.user_group_name)

        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )

        print("Accepting WebSocket")

        await self.accept()

        print("WebSocket accepted")

    async def disconnect(self, close_code):
        print("WebSocket disconnected:", close_code)

        if hasattr(self, "user_group_name"):
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )

    async def notification_message(self, event):
        await self.send_json({
            "type": "notification",
            "message": event["message"],
        })