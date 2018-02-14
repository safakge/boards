# use
# exec(open('scratch.py').read())
# to run this
from django.contrib.auth.models import User
from django.utils.crypto import random

from boards.models import Board, Topic, Post
from django.core.paginator import Paginator

print('Started executing scratch...')


def add_posts_to_topic(board_id, topic_id, count=10):
    topic = Topic.objects.get(board_id=board_id, id=topic_id)

    randval = random.randint(1000, 10000)
    for i in range(0, 10):
        msg = f'post {randval}{i} for topic {board_id}-{topic_id}'
        print(msg)
        user = User.objects.first()
        post = Post.objects.create(message=msg, created_by=user, topic=topic).save()


def paginate():
    queryset = Topic.objects.filter(board_id=6).order_by('last_updated')
    paginator = Paginator(queryset, 20)
    return paginator


print('scratch ended.')
