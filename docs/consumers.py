import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Documents

class DocumentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.document_slug = self.scope['url_route']['kwargs']['document_slug']
        self.group_name = f'document_{self.document_slug}'

        await self.channel_layer.group_add(
            self.group_name,self.channel_name
        )

        await self.accept()

    async def disconnect(self,_):
        await self.channel_layer.group_discard(self.group_name,self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        document_content = data['document_content']
        document_name = data['document_name']
        position = data.get('position', None)
        user = data['user']

        await self.save_changes(self.document_slug,document_content)
        
        

        if document_name:
            is_creator = await self.check_creator(self.document_slug,user)
            if is_creator:
                await self.save_name(self.document_slug,document_name)

        await self.channel_layer.group_send(
            self.group_name,
            {
            'type': 'document_update',
            'document_content': document_content,
            'document_name': document_name,
            'position': position,
            'user': user,
            }
        )

    async def document_update(self,event):
        document_content = event['document_content']
        position = event.get('position', None)
        user = event['user']
        document_name = event['document_name']

        await self.send(text_data=json.dumps({
        'document_content': document_content,
        'document_name': document_name,
        'position': position,
        'user': user
        }))

    @sync_to_async
    def save_changes(self,slug,content):
        document = Documents.objects.get(slug=slug)
        document.content = content
        document.save()

    @sync_to_async
    def save_name(self,slug,name):
        document = Documents.objects.get(slug=slug)
        document.name = name
        document.save()     

    @sync_to_async
    def check_creator(self,slug,user):
        document = Documents.objects.get(slug=slug)
        return document.creator.username == user

