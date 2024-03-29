import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from djangochannelsrestframework.consumers import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    room_name = None

    async def connect(self):
        user_id = self.scope['user'].id
        self.room_name = f'notification_{user_id}'
        await self.channel_layer.group_add(
            self.room_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name, self.channel_name
        )

    async def send_notification(self, event):
        message = event["message"]
        await self.send_json(message)


def send_notification(user_id, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notification_{user_id}', {
            'type': 'send.notification',
            'message': json.loads(json.dumps(data)),
        }
    )