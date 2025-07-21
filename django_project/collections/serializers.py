from rest_framework import serializers
from .models import Collection
from posts.serializers import PostSerializer

class CollectionSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Collection
        fields = ['id', 'name', 'owner', 'posts', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class CollectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['name'] 