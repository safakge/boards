from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from boards.forms import NewTopicForm
from boards.models import Topic, Post, Board
from boards.views import new_topic


class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='TestBoard', description='Testiness board.')
        User.objects.create_user(username='john', email='john@doe.com', password='123')

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'board_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'board_id': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_correct_view(self):
        view = resolve('/board/1/new')
        self.assertEqual(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        url = reverse('new_topic', kwargs={'board_id': 1})
        response = self.client.get(url)
        board_url = reverse('board_topics', kwargs={'board_id': 1})
        self.assertContains(response, 'href="{0}"'.format(board_url))

    def test_csrf(self):
        url = reverse('new_topic', kwargs={'board_id': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'board_id': 1})
        data = {
            'subject': 'sbj',
            'message': 'msg'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'board_id': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_empty_post_data(self):
        url = reverse('new_topic', kwargs={'board_id': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        url = reverse('new_topic', kwargs={'board_id': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)
