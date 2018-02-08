from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from accounts.forms import SignUpForm
from accounts.views import signup


class SignupTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup')
        self.assertEqual(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        """
        The view must contain five inputs: csrf, username, email,
        password1, password2
        """
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignupTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'test',
            'email': 'asde@gmail.com',
            'password1': 'abcabcabc',
            'password2': 'abcabcabc'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirection(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        """
        Create a new request to an arbitrary page.
        The resulting response should now have a `user` to its context,
        after a successful sign up.
        """
        url = reverse('home')
        response = self.client.get(url)
        user: User = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignupTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})  # post empty data

    def test_signup_status_code(self):
        """
        must not redirect
        """
        self.assertTrue(self.response.status_code, 200)

    def test_form_errors(self):
        """
        form must throw errors
        """
        form: SignUpForm = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_no_user_creation(self):
        self.assertFalse(User.objects.exists())
