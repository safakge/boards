from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from boards.views import home, board_topics, new_topic
from boards.models import Board, Topic, Post


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Test board', description='a board')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'board_id': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='TestBoard', description='Testiness board.')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'board_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'board_id': 234})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/board/1')
        self.assertEqual(view.func, board_topics)

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'board_id': 1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'board_id': 1})
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))


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
        self.assertEquals(response.status_code, 200)

    def test_new_topic_empty_post_data(self):
        url = reverse('new_topic', kwargs={'board_id': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())
