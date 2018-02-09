import email

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from boards.models import Board, Topic, Post
from boards.views import topic_posts


class TopicPostsTests(TestCase):
    def setUp(self):
        board = Board.objects.create(name='Test board', description='test board desc')
        user = User.objects.create_user('bill', email='a@b.com', password='abc123456')
        topic = Topic.objects.create(subject='Hello', board=board, starter=user)
        Post.objects.create(message='First post!', topic=topic, created_by=user)
        url = reverse('topic_posts', kwargs={'board_id': board.id, 'topic_id': topic.id})
        self.response = self.client.get(url)
        pass

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/board/1/topics/1/')
        self.assertEqual(view.func, topic_posts)
