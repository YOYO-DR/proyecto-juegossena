from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Unirse al grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recibir mensaje desde WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user=text_data_json.get('user',None)

        # Enviar mensaje al grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                "user":user
            }
        )
        # ejecuto con el await la funcion que cree
        await self.post_message(text_data_json)

    # Recibir mensaje desde el grupo
    async def chat_message(self, event):
        message = event['message']
        user=event.get('user',None)

        # Enviar mensaje a WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            "user":user
        }))
    # convierte lo que este dentro sobre bd o rl orm, en operaciones asincronas
    @database_sync_to_async
    def post_message(self, data):
        try:
          from apps.usuarios.models import Usuario
          from apps.chat.models import HistorialChat
          user = Usuario.objects.get(username=data['user'])
          HistorialChat.objects.create(user=user,message=data['message'])
        except Exception as e:
            # si sale algun error, o el error de que no han cargado las aplicaciones, lo paso para que cargue todo normal
            print(str(e))