from django.shortcuts import render, get_object_or_404
from .models import NewsPost

def news_list(request):
    posts = NewsPost.objects.order_by('-pub_date')  # самые свежие сверху
    return render(request, 'news/news_list.html', {'posts': posts})

def news_detail(request, pk):
    post = get_object_or_404(NewsPost, pk=pk)
    return render(request, 'news/news_detail.html', {'post': post})

def home(request):
    return render(request, 'news/home.html')

def about(request):
    return render(request, 'news/about.html')

def contacts(request):
    return render(request, 'news/contacts.html')

def gallery(request):
    return render(request, 'news/gallery.html')