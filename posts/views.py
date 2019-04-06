from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post, Author
from .forms import CommentForm, PostForm

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def index(request):
    latest = Post.objects.order_by('-timestamp')[:4]
    context = {
        'latest': latest,
    }
    return render(request, 'index.html', context)

def blog(request):
    post_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(post_list, 6)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'page_request_var': page_request_var,
        'post_list': paginated_queryset,
    }
    return render(request, 'blog-grid.html', context)

def post(request, id):
    post = get_object_or_404(Post, id=id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.post = post
            form.save()
            return redirect(reverse('post_detail', kwargs={
                'id': post.id,
            }))
    context = {
        'form': form,
        'post': post
    }
    return render(request, 'blog-single.html', context)

def post_create(request):
    title = 'Create'
    author = get_author(request.user)
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post_detail', kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }

    return render(request, 'post-create.html', context)

def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    author = get_author(request.user)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post_detail', kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }

    return render(request, 'post-create.html', context)

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse('post_list'))