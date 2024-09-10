from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/<str:document_slug>/',consumers.DocumentConsumer.as_asgi()),
]