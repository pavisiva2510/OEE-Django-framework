
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Video

class VideoTestCase(TestCase):

    def setUp(self): 
        self.user = User.objects.create(username='testuser')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_video(self):
        data = {'name': 'Test Video', 'video_url': 'https://example.com/video.mp4'}
        response = self.client.post('/api/videos/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Video.objects.count(), 1)
        self.assertEqual(Video.objects.get().name, 'Test Video')

    def test_delete_video(self):
        video = Video.objects.create(user=self.user, name='Test Video', video_url='https://example.com/video.mp4')
        response = self.client.delete(f'/api/videos/{video.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Video.objects.count(), 0)


