from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from .models import Group, Post, Follow, User
from .forms import CommentForm, PostForm
from .paginator import paginator


def group_posts(request, slug_name):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug_name)
    post_list = group.posts.all()
    context = {
        'group': group,
        'page_obj': paginator(request, post_list),
    }
    return render(request, template, context)


def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.select_related('group', 'author').all()
    context = {
        'page_obj': paginator(request, post_list),
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    post_list = author.author.all()
    follow_status = False
    if request.user.is_authenticated:
        if Follow.objects.filter(author=author, user=request.user).exists():
            follow_status = True
    context = {
        'author': author,
        'page_obj': paginator(request, post_list),
        'following': follow_status,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    comments = post.comment.all()
    counter = Post.objects.filter(author=post.author).count
    context = {
        'post': post,
        'counter': counter,
        'form': form,
        'comments': comments,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('posts:profile', username=request.user)
    form = PostForm(request.POST or None, files=request.FILES or None)
    context = {
        'form': form
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(
                request.POST or None,
                files=request.FILES or None,
                instance=post
            )
            if form.is_valid():
                edit_post = form.save(commit=False)
                edit_post.author = request.user
                edit_post.save()
                return redirect('posts:post_detail', post_id=post_id)
        form = PostForm(
            request.POST or None,
            files=request.FILES or None,
            instance=post
        )
        is_edit = True
        context = {
            'form': form,
            'is_edit': is_edit
        }
        return render(request, template, context)
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    template = 'posts/follow.html'
    post_list = Post.objects.filter(author__following__user=request.user)
    context = {
        'page_obj': paginator(request, post_list),
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        if not Follow.objects.filter(
                author=author, user=request.user).exists():
            Follow.objects.create(
                author=author, user=request.user)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    if Follow.objects.filter(author=author, user=request.user).exists():
        author.following.filter(user=request.user).delete()
    return redirect('posts:profile', username=username)
