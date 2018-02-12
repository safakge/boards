from django.contrib.auth.models import User
from django.db import models
from typing import *

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
