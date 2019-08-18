from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post, Author, Comment
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
    comments = post.comments.filter(parent__isnull=True)


    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    comment_reply = form.save(commit=False)
                    comment_reply.parent = parent_obj
            form.instance.post = post
            form.save()
            return redirect(reverse('post_detail', kwargs={
                'id': post.id,
            }))
    context = {
        'form': form,
        'post': post,
        'comments': comments
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
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            # form.instance.author = author
            form.save()
            return redirect(reverse('post_detail', kwargs={
                'id': post.id
            }))
    else:
        form = PostForm(instance=post)

    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'post-create.html', context)

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse('post_list'))