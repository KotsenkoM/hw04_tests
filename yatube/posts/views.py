from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts,
        'paginator': paginator,
        'page': page,
    }
    return render(request, 'group.html', context)


@login_required()
def new_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('index')
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    author_posts = author.posts.all()
    paginator = Paginator(author_posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    post_count = author.posts.count()
    print(author)
    context = {
        'author': author,
        'page': page,
        'post_count': post_count,
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    author = post.author
    return render(request, 'post.html', {"post": post, "author": author})


@login_required()
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    form = PostForm(request.POST or None, instance=post)
    if not post:
        return redirect('index')
    if request.user != post.author:
        return redirect('post', username, post_id)
    if request.method != 'POST':
        return render(
            request, "new_post.html", {"form": form, "post": post})
    if form.is_valid():
        form.save()
        return redirect('post', username, post_id)
    return render(
        request, "new_post.html", {"form": form, "post": post})


def add_comment(request, username, post_id):
    form = PostForm(request.POST or None)
    post = get_object_or_404(Post, author__username=username, id=post_id)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('post', username, post_id)
