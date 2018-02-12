from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from boards import views, forms
from boards.models import Board, Topic, Post


class ReplyTopicTestCase(TestCase):
    """
    Base test case to be used in all `reply_topic` view tests (without auth)
    """

    def setUp(self):
        self.board = Board.objects.create(name='Test board', description='a test board')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(self.username, email='abc@def.com', password=self.password)
        self.topic = Topic.objects.create(subject='Test topic', board=self.board, starter=user)
        Post.objects.create(created_by=user, topic=self.topic, message='Test post')
        self.url = reverse('reply_topic', kwargs={'board_id': self.board.id, 'topic_id': self.topic.id})


class ReplyTopicWithAuthTestCase(ReplyTopicTestCase):
    """
    Base setUp + login
    """

    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)


class LoginRequiredReplyTopicTests(ReplyTopicTestCase):
    def test_redirection(self):
        response = self.client.get(self.url)
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class ReplyTopicTests(ReplyTopicWithAuthTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_view_function(self):
        view = resolve('/board/1/topics/1/reply')
        self.assertEqual(view.func, views.reply_topic)
        
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, forms.PostForm)

    def test_form_inputs(self):
        """
        The view must contain two inputs: csrf, message textarea
        """
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)

class SuccessfulReplyTopicTests(ReplyTopicWithAuthTestCase):
    # ...
    pass


class InvalidReplyTopicTests(ReplyTopicWithAuthTestCase):
    # ...
    pass
