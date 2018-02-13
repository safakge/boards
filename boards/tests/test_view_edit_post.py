from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from boards.models import Board, Topic, Post


class PostUpdateViewTestCase(TestCase):
    def setUp(self):
        print('PostUpdateViewTestCase setup...')
        self.board = Board.objects.create(name='Test board', description='a test board')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(self.username, email='abc@def.com', password=self.password)
        self.topic = Topic.objects.create(subject='Test topic', board=self.board, starter=user)
        self.post = Post.objects.create(created_by=user, topic=self.topic, message='Test post')
        self.url = reverse('edit_post',
                           kwargs={'board_id': self.board.id, 'topic_id': self.topic.id, 'post_id': self.post.id})


class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):
    def test_redirection(self):
        response = self.client.get(self.url)
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={self.url}')
