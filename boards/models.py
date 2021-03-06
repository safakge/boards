import math
from django.contrib.auth.models import User
from django.db import models
from typing import *

from django.utils.safestring import mark_safe
from markdown import markdown

from django.utils.text import Truncator


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

    def __str__(self):
        return f"#{self.id} - {self.name}"


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"#{self.id} - {self.subject}"

    @staticmethod
    def paginated_post_count():
        return 10

    def get_page_count(self):
        count = self.posts.count()
        pages = count / Topic.paginated_post_count()
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, int(count + 1))  # int cast is to silence a warning, which may be incorrect

    def get_last_10_posts(self):
        return self.posts.order_by('-created_at')[:10]


class Post(models.Model):
    message = models.CharField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, default='No one', related_name='posts', on_delete=models.SET_DEFAULT)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL)

    def __str__(self):
        truncated = Truncator(self.message)
        return f"#{self.id} - {truncated.chars(30)}"

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
