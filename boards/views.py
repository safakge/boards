from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import UpdateView

from boards.forms import NewTopicForm, PostForm
from .models import Board, Topic, Post


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


def about(request):
    return HttpResponse('{} '.format(request.get_full_path()))


def board_topics(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board': board, 'topics': topics})


@login_required
def new_topic(request, board_id):
    board = get_object_or_404(Board, pk=board_id)

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', board_id=board.pk, topic_id=topic.id)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board_id=board_id, id=topic_id)
    topic.view_count += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board_id=board_id, id=topic_id)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', board_id=board_id, topic_id=topic_id)
    else:
        form = PostForm()

    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


class PostUpdateView(UpdateView):
    model = Post

    fields = ('message',)  # we have the option to either define form_class or the fields attribute.
    # In the example above we are using the fields attribute to create a model form on-the-fly. Internally, Django will use a model form factory to
    #  compose a form of the Post model. Since it’s a very simple form with just the message field, we can afford to work like this. But for
    # complex form definitions, it’s better to define a model form externally and refer to it here.

    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_id'  # identify the name of the keyword argument used to retrieve the Post object. It’s the same as we define in the urls.py
    context_object_name = 'post' # If we don’t set the context_object_name attribute, the Post object will be available in the template as
    # “object.” So, here we are using the context_object_name to rename it to post instead. You will see how we are using it in the template below.

    def get_form(self, form_class=None):
        form = super(PostUpdateView, self).get_form(form_class)
        form.fields['message'].widget = forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Edit your post'}
        )
        return form

    def form_valid(self, form):
        # In this particular example, we had to override the form_valid() method so as to set some extra fields such as the updated_by and updated_at.
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', board_id=post.topic.board.id, topic_id=post.topic.id)
