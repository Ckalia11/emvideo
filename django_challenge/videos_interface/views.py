import re
from turtle import title
from django.http import HttpResponse
from django.shortcuts import render
from .models import Video, Comment, Clicks
from .forms import CommentForm
from django.contrib import messages


# Create your views here.

def videos_interface(request):
    if request.method == 'GET':
        objs = Video.objects.all()        
    return render(request, 'videos_interface/videos_interface.html', {'objs': objs})

def video_detail(request, pk):
    video = Video.objects.get(pk=pk)
    videos = Video.objects.all()
    comments = Comment.objects.filter(video = video)

    if request.method == 'GET':
        if Clicks.objects.filter(user=request.user,video=video).exists():
            click = Clicks.objects.get(user=request.user,video=video)
            click.clicks = click.clicks + 1
        else:
            click = Clicks.objects.create(user=request.user,video=video,clicks=1)
        click.save()
        form = CommentForm()
    elif request.method == 'POST':
        print(request.POST)
        form = CommentForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Comment was saved.')
            comment = Comment.objects.create(comment=form.cleaned_data['comment'], user = request.user, video = video)
            comment.save()
        else:
            print(form.errors)
    return render(request, 'videos_interface/video.html', {'video': video, 'form': form, 'videos': videos, 'comments':comments})

    
