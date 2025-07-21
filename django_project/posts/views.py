from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            post = serializer.save()
            self._notify_websocket('post_created', post)

    def perform_update(self, serializer):
        with transaction.atomic():
            post = serializer.save()
            self._notify_websocket('post_updated', post)

    def perform_destroy(self, instance):
        post_id = instance.id
        with transaction.atomic():
            instance.delete()
            self._notify_websocket('post_deleted', {'id': post_id})

    def _notify_websocket(self, event_type, data):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'notification.message',
                'message': {
                    'event_type': event_type,
                    'data': PostSerializer(data).data if hasattr(data, 'id') else data
                }
            }
        ) 