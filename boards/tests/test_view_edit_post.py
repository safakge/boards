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
    def test_redirection_if_not_logged_in(self):
        response = self.client.get(self.url)
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class UnauthorizedPostUpdateViewTests(PostUpdateViewTestCase):
    """
    Post edit attempt done by a user who isn't the author
    """

    def setUp(self):
        super().setUp()
        username, password = 'naughtyuser', '321'
        User.objects.create_user(username, password=password, email='naughty@user.com')
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        """
        A topic should be edited only by the owner.
        Unauthorized users should get a 404 response (Page Not Found)
        """
        self.assertEquals(self.response.status_code, 404)
