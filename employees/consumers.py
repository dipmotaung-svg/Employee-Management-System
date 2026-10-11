import json

from channels.generic.websocket import AsyncWebsocketConsumer


class EmployeeNotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(
            "employee_updates",
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_discard(
                "employee_updates",
                self.channel_name
            )

    async def employee_updated(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))