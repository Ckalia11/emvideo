import re
from turtle import title
from django.http import HttpResponse
from django.shortcuts import render
from .models import Video, Comment, Clicks
from .forms import CommentForm, VideoForm
from django.contrib import messages


# Create your views here.

def videos(request):
    if request.method == 'GET':
        videos = Video.objects.all()       
    return render(request, 'videos_interface/videos.html', {'videos': videos})

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

def my_videos(request):
    if request.method == 'GET':
        try:
            videos = Video.objects.get(user = request.user)
        except Video.DoesNotExist:
            videos = None
    return render(request, 'videos_interface/my_videos.html', {'videos': videos})

def create_video(request):
    if request.method == "GET":
        form = VideoForm()
    elif request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
    context= {
              'form': form
              }   
    return render(request, 'videos_interface/create_video.html', context)

    

    
