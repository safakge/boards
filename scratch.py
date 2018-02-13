# use
# exec(open('scratch.py').read())
# to run this
from django.contrib.auth.models import User
from boards.models import Board, Topic, Post
from django.core.paginator import Paginator

print('Started executing scratch...')


def paginate():
    queryset = Topic.objects.filter(board_id=6).order_by('last_updated')
    paginator = Paginator(queryset, 20)
    return paginator

print('scratch ended.')
