from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import CommentForm

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
    context = {
        'form': form,
        'post': post
    }
    return render(request, 'blog-single.html', context)