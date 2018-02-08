from django import forms
from django.test import TestCase

from boards.templatetags import form_tags


class ExampleForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ('name', 'password')


class FieldTypeTests(TestCase):
    def test_field_widget_type(self):
        form = ExampleForm()
        self.assertEqual('TextInput', form_tags.field_type(form['name']))
        self.assertEqual('PasswordInput', form_tags.field_type(form['password']))


class InputClassTests(TestCase):
    def test_unbound_field_initial_state(self):
        form = ExampleForm()
        self.assertEqual('form-control ', form_tags.input_class(form['name']))

    def test_valid_bound_field(self):
        form = ExampleForm({'name': 'a', 'password': '123'})
        self.assertEqual('form-control is-valid', form_tags.input_class(form['name']))
        self.assertEqual('form-control ', form_tags.input_class(form['password']))

    def test_invalid_bound_field(self):
        form = ExampleForm({'name': '', 'password': '123'})
        self.assertEqual('form-control is-invalid', form_tags.input_class(form['name']))
        self.assertEqual('form-control ', form_tags.input_class(form['password']))
