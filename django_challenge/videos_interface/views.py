from msilib.schema import Error
import re
from turtle import title
from urllib.error import HTTPError
from xml.dom import ValidationErr
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Video, Comment, Clicks, Thumbnail
from .forms import CommentForm, VideoForm
from django.contrib import messages
import os
import cv2
from django.core.files import File  
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.utils import IntegrityError






# Create your views here.

def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse("videos"))
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("videos"))
        else:
            messages.error(request, "Invalid username or password")
    context = {}
    return render(request, "videos_interface/login.html", context)

def logout_view(request):
    logout(request)
    return redirect(reverse("login"))

def create_account_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            user = User.objects.create_user(username = username, email = email, password = password)
            login(request, user)
            return redirect(reverse("videos"))
        except IntegrityError:
            messages.error(request, "An account with this information exists. Please login.")
    return render(request, "videos_interface/create_account.html", {})

def videos(request):
    logged_in = False
    if not request.user.is_anonymous:
        logged_in = True
    videos = Video.objects.all()  
    if not videos:
        messages.info(request, 'There are no videos.')
    for video in videos:
        get_thumbnail(video)
    thumbnails = Thumbnail.objects.all()
    context = {"thumbnails": thumbnails, "logged_in": logged_in}
    return render(request, 'videos_interface/videos.html', context)

def my_videos(request):
    videos = Video.objects.filter(user = request.user)
    for video in videos:
        get_thumbnail(video)
    thumbnails = Thumbnail.objects.all()
    if not videos:
        messages.info(request, "You haven't created any videos.")
    context = {"thumbnails": thumbnails}
    return render(request, 'videos_interface/my_videos.html', context)

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
            return redirect(reverse("my_videos"))
    context= {
              'form': form
              }   
    return render(request, 'videos_interface/create_video.html', context)

def video_detail(request, pk):
    if request.method == 'GET':
        try:
            video = Video.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404("Video does not exist")
        videos = Video.objects.all()
        # comments = Comment.objects.filter(video = video)
        form = CommentForm()
        # add_click(request)
    elif request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            messages.success(request, "Comment was saved.")
            comment = form.cleaned_data['comment']
            comment_object = Comment.objects.create(comment=comment, user = request.user, video = video)
        else:
            print(form.errors)
    context = {'video': video, 'form': form, 'videos': videos}
    return render(request, 'videos_interface/video.html', context)

def my_video_detail(request, pk):
    video = Video.objects.get(pk=pk)
    context = {'video':video}
    return render(request, "videos_interface/my_video_detail.html", context)    

def my_video_edit(request, pk):
    video = Video.objects.get(pk=pk)
    if request.method == "GET":
        form = VideoForm(instance=video)
        context = {'form': form}
        return render(request, 'videos_interface/my_video_edit.html', context)
    elif request.method == "POST":
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            video.title = form.cleaned_data.get("title")
            video.videofile = form.cleaned_data.get("videofile")
            video.user = request.user
            video.save()
            return redirect("my_videos")

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

def add_click(request):
    if Clicks.objects.filter(user=request.user,video=video).exists():
        click = Clicks.objects.get(user=request.user,video=video)
        click.clicks = click.clicks + 1
        click.save()
    else:
        click = Clicks.objects.create(user=request.user,video=video,clicks=1)
        



    


    

    
