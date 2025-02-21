import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from djangochannelsrestframework.consumers import AsyncJsonWebsocketConsumer


class CILConsumer(AsyncJsonWebsocketConsumer):
    room_name = None

    async def connect(self):
        cil_id = self.scope['url_route']['kwargs']['cil_id']
        self.room_name = f'camera_{cil_id}'
        await self.channel_layer.group_add(
            self.room_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name, self.channel_name
        )

    async def send_cil(self, event):
        message = event["message"]
        await self.send_json(message)


def send_data_cil(cit_id, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'camera_{cit_id}', {
            'type': 'send.cil',
            'message': json.loads(json.dumps(data)),
        }
    )