from django.urls import path
from inventory import consumers

websocket_urlpatterns = [
    path('ws/orders/', consumers.OrderConsumer.as_asgi()),  # URL for WebSocket connection
]