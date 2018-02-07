from typing import List

from django.test import TestCase

from accounts.forms import SignUpForm


class SignUpFormTests(TestCase):

    def test_form_has_fields(self):
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2']
        actual: List = list(form.fields)
        self.assertEqual(expected, actual)
