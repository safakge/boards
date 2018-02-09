from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LoginRequiredPasswordChangeTests(TestCase):
    def test_redirection(self):
        url = reverse('password_change')
        login_url = reverse('login')
        response = self.client.get(url)

        self.assertRedirects(response, f'{login_url}?next={url}')


class PasswordChangeTestCase(TestCase):
    def setUp(self, data={}):
        self.user = User.objects.create_user('bill', email='a@b.com', password='abc123123')
        self.url = reverse('password_change')
        self.client.login(username=self.user.username, password='abc123123')
        self.response = self.client.post(self.url, data)


class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self, **kwargs):
        super().setUp({
            'old_password': 'abc123123',
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        })

    def test_redirection(self):
        """
        A valid form submission should redirect the user
        """
        self.assertRedirects(self.response, reverse('password_change_done'))

    def test_password_changed(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authentication(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertTrue(response.context.get('user').is_authenticated)


class DeniedPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self, **kwargs):
        super().setUp({
            'old_password': 'WRONG_OLD_PASSWORD',
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        })

    def test_status_code(self):
        """
        Invalid submission should not authenticate
        """
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        self.user.refresh_from_db()
        self.assertTrue(not self.user.check_password('new_password'))

    def test_user_not(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertTrue(response.context.get('user').is_authenticated)
