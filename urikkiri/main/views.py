from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Content
from .forms import ContentForm, CommentForm
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    posts = Content.objects.all
    return render(request, 'main/home.html', {'posts_list':posts})

def new(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('home')
    else:
        form = ContentForm()
    
    return render(request, 'main/new.html', {'form':form})

def detail(request, index):
    post = get_object_or_404(Content, pk=index)
    return render(request, 'main/detail.html', {'post':post})

def edit(request, index):
    post = get_object_or_404(Content, pk=index)
    if request.method == 'POST':
        form = ContentForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('detail', index=post.pk)
    else:
        form = ContentForm(instance=post)
    return render(request, 'main/edit.html', {'form': form})

def delete(request, pk):
    post = get_object_or_404(Content, pk=pk)
    post.delete()
    return redirect('home')

def add_comment(request, pk):
    post = get_object_or_404(Content, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('detail', index=post.pk)
    else:
        form = CommentForm()
    return render(request, 'main/add_comment.html', {'form': form})