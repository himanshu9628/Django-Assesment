from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post
from .serializers import PostSerializer

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_post_creation(self):
        post = Post.objects.create(
            title='Test Post',
            body='This is a test post body',
            author=self.user
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.body, 'This is a test post body')
        self.assertEqual(post.author, self.user)
        
    def test_post_str_representation(self):
        post = Post.objects.create(
            title='Test Post',
            body='This is a test post body',
            author=self.user
        )
        self.assertEqual(str(post), 'Test Post')

class PostAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_create_post(self):
        url = reverse('post-list')
        data = {
            'title': 'New Post',
            'body': 'This is a new post'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'New Post')
        
    def test_list_posts(self):
        Post.objects.create(
            title='Post 1',
            body='Body 1',
            author=self.user
        )
        Post.objects.create(
            title='Post 2',
            body='Body 2',
            author=self.user
        )
        
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_get_post_detail(self):
        post = Post.objects.create(
            title='Test Post',
            body='Test Body',
            author=self.user
        )
        url = reverse('post-detail', args=[post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')
        
    def test_update_post(self):
        post = Post.objects.create(
            title='Original Title',
            body='Original Body',
            author=self.user
        )
        url = reverse('post-detail', args=[post.id])
        data = {
            'title': 'Updated Title',
            'body': 'Updated Body'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Title')
        
    def test_delete_post(self):
        post = Post.objects.create(
            title='Test Post',
            body='Test Body',
            author=self.user
        )
        url = reverse('post-detail', args=[post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

class PostSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_post_serializer(self):
        post = Post.objects.create(
            title='Test Post',
            body='Test Body',
            author=self.user
        )
        serializer = PostSerializer(post)
        data = serializer.data
        self.assertEqual(data['title'], 'Test Post')
        self.assertEqual(data['body'], 'Test Body')
        self.assertEqual(data['author'], self.user.id) 