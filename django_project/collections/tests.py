from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Collection
from posts.models import Post
from .serializers import CollectionSerializer

class CollectionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_collection_creation(self):
        collection = Collection.objects.create(
            name='Test Collection',
            owner=self.user
        )
        self.assertEqual(collection.name, 'Test Collection')
        self.assertEqual(collection.owner, self.user)
        
    def test_collection_str_representation(self):
        collection = Collection.objects.create(
            name='Test Collection',
            owner=self.user
        )
        expected_str = f"Test Collection (by {self.user.username})"
        self.assertEqual(str(collection), expected_str)
        
    def test_collection_posts_relationship(self):
        collection = Collection.objects.create(
            name='Test Collection',
            owner=self.user
        )
        post = Post.objects.create(
            title='Test Post',
            body='Test Body',
            author=self.user
        )
        collection.posts.add(post)
        self.assertIn(post, collection.posts.all())

class CollectionAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_create_collection(self):
        url = reverse('collection-list')
        data = {
            'name': 'New Collection'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Collection.objects.count(), 1)
        self.assertEqual(Collection.objects.get().name, 'New Collection')
        self.assertEqual(Collection.objects.get().owner, self.user)
        
    def test_list_collections(self):
        Collection.objects.create(
            name='Collection 1',
            owner=self.user
        )
        Collection.objects.create(
            name='Collection 2',
            owner=self.user
        )
        
        url = reverse('collection-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_get_collection_detail(self):
        collection = Collection.objects.create(
            name='Test Collection',
            owner=self.user
        )
        url = reverse('collection-detail', args=[collection.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Collection')
        
    def test_update_collection(self):
        collection = Collection.objects.create(
            name='Original Name',
            owner=self.user
        )
        url = reverse('collection-detail', args=[collection.id])
        data = {
            'name': 'Updated Name'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        collection.refresh_from_db()
        self.assertEqual(collection.name, 'Updated Name')
        
    def test_delete_collection(self):
        collection = Collection.objects.create(
            name='Test Collection',
            owner=self.user
        )
        url = reverse('collection-detail', args=[collection.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Collection.objects.count(), 0)
        
    def test_add_post_to_collection(self):
        collection = Collection.objects.create(
            name='Test Collection',
            owner=self.user
        )
        post = Post.objects.create(
            title='Test Post',
            body='Test Body',
            author=self.user
        )
        
        url = reverse('collection-add-post', args=[collection.id])
        data = {'post_id': post.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(post, collection.posts.all())
        
    def test_remove_post_from_collection(self):
        collection = Collection.objects.create(
            name='Test Collection',
            owner=self.user
        )
        post = Post.objects.create(
            title='Test Post',
            body='Test Body',
            author=self.user
        )
        collection.posts.add(post)
        
        url = reverse('collection-remove-post', args=[collection.id])
        data = {'post_id': post.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(post, collection.posts.all())
        
    def test_add_nonexistent_post_to_collection(self):
        collection = Collection.objects.create(
            name='Test Collection',
            owner=self.user
        )
        
        url = reverse('collection-add-post', args=[collection.id])
        data = {'post_id': 999}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CollectionSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_collection_serializer(self):
        collection = Collection.objects.create(
            name='Test Collection',
            owner=self.user
        )
        serializer = CollectionSerializer(collection)
        data = serializer.data
        self.assertEqual(data['name'], 'Test Collection')
        self.assertEqual(data['owner'], self.user.username)
        self.assertEqual(data['posts'], [])
        
    def test_collection_with_posts_serializer(self):
        collection = Collection.objects.create(
            name='Test Collection',
            owner=self.user
        )
        post = Post.objects.create(
            title='Test Post',
            body='Test Body',
            author=self.user
        )
        collection.posts.add(post)
        
        serializer = CollectionSerializer(collection)
        data = serializer.data
        self.assertEqual(len(data['posts']), 1)
        self.assertEqual(data['posts'][0]['title'], 'Test Post') 