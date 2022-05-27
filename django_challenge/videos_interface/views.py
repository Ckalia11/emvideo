import re
from turtle import title
from django.http import HttpResponse
from django.shortcuts import render
from .models import Video, Comment, Clicks, Thumbnail
from .forms import CommentForm, VideoForm
from django.contrib import messages
import os
from os import listdir
from os.path import isfile, join
import cv2
from django.core.files import File  





# Create your views here.

def videos(request):
    if request.method == 'GET':
        videos = Video.objects.all()  
        for video in videos:
            get_thumbnail(video)
        thumbnails = Thumbnail.objects.all()
        context = {"videos": videos, "thumbnails": thumbnails}
    # return HttpResponse('yo')
    return render(request, 'videos_interface/videos.html', context)

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
    print("REQUEST", request.user)
    if request.method == 'GET':
        try:
            videos = Video.objects.filter(user = request.user)
        except Video.DoesNotExist:
            videos = None
        print("VIDEOS", type(videos))
    return render(request, 'videos_interface/my_videos.html', {'videos': videos})

def create_video(request):
    if request.method == "GET":
        form = VideoForm()
    elif request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            videofile = form.cleaned_data.get("videofile")
            user = request.user
            video = Video.objects.create(title = title, videofile = videofile, user = user)
            video.save()
    context= {
              'form': form
              }   
    return render(request, 'videos_interface/create_video.html', context)

def get_thumbnail(video):
    try:
        _ = Thumbnail.objects.get(video = video)
    # generate image
    except Thumbnail.DoesNotExist:
        video_path = str(video.videofile)
        input_path = os.path.join('media', video_path)
        vidcap = cv2.VideoCapture(input_path)
        success, image = vidcap.read()
        output_path = os.path.join('media','images', str(video.pk) + '.jpg')
        cv2.imwrite(output_path, image) 
        # save image
        thumb = Thumbnail.objects.create(image = File(open(output_path, 'rb')), video = video)
        thumb.save()
        



    


    

    
