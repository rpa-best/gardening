import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from djangochannelsrestframework.consumers import AsyncJsonWebsocketConsumer
from oauth.consumers import send_notification


class CameraConsumer(AsyncJsonWebsocketConsumer):
    room_name = None

    async def connect(self):
        camera_id = self.scope['user'].id
        self.room_name = f'camera_{camera_id}'
        await self.channel_layer.group_add(
            self.room_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name, self.channel_name
        )

    async def send_datacamera(self, event):
        message = event["message"]
        await self.send_json(message)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        text_data_json = json.loads(text_data)
        user_id = text_data_json.get("user_id")
        if user_id:
            await database_sync_to_async(send_notification)(user_id, {
                "type": "success",
                "data": text_data_json
            })
        

def send_data_camera(id, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'camera_{id}', {
            'type': 'send.datacamera',
            'message': json.loads(json.dumps(data)),
        }
    )