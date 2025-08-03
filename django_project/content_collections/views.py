from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from posts.models import Post

from .models import Collection
from .serializers import CollectionSerializer, CollectionCreateSerializer

class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CollectionCreateSerializer
        return CollectionSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            collection = serializer.save(owner=self.request.user)
            self._notify_websocket('collection_created', collection)

    def perform_update(self, serializer):
        with transaction.atomic():
            collection = serializer.save()
            self._notify_websocket('collection_updated', collection)

    def perform_destroy(self, instance):
        collection_id = instance.id
        with transaction.atomic():
            instance.delete()
            self._notify_websocket('collection_deleted', {'id': collection_id})

    @action(detail=True, methods=['post'])
    def add_post(self, request, pk=None):
        collection = self.get_object()
        post_id = request.data.get('post_id')
        
        try:
            post = Post.objects.get(id=post_id)
            collection.posts.add(post)
            self._notify_websocket('post_added_to_collection', {
                'collection_id': collection.id,
                'post_id': post.id
            })
            return Response({'status': 'post added'})
        except Post.DoesNotExist:
            return Response(
                {'error': 'Post not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def remove_post(self, request, pk=None):
        collection = self.get_object()
        post_id = request.data.get('post_id')
        
        try:
            post = Post.objects.get(id=post_id)
            collection.posts.remove(post)
            self._notify_websocket('post_removed_from_collection', {
                'collection_id': collection.id,
                'post_id': post.id
            })
            return Response({'status': 'post removed'})
        except Post.DoesNotExist:
            return Response(
                {'error': 'Post not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def _notify_websocket(self, event_type, data):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'notification.message',
                'message': {
                    'event_type': event_type,
                    'data': CollectionSerializer(data).data if hasattr(data, 'id') else data
                }
            }
        ) 