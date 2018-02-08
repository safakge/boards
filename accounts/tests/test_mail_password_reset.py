from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase


class PasswordResetMailTests(TestCase):
    test_user_email = 'john@doe.com'

    def setUp(self):
        """
        create a password reset request for a given user
        """
        User.objects.create_user(username='john', email=self.test_user_email, password='123')
        self.response = self.client.post(reverse('password_reset'), {'email': self.test_user_email})
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertIn('Please reset your password', self.email.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})

        # we use assertIn here, because assertContains is only for HttpResponses they say
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('john', self.email.body)
        self.assertIn(self.test_user_email, self.email.body)

    def test_email_to(self):
        self.assertEqual([self.test_user_email, ], self.email.to)
