from http.client import HTTPResponse
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
import regex as re
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from django.core.validators import validate_email



EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

# Create your views here.

def login_view(request):
    logged_in = False
    context = {}
    if request.method == "GET":
        if request.user.is_authenticated:
            logged_in = True
            user_id = request.session.get('_auth_user_id')
            user = User.objects.get(pk=user_id)
            first_name = user.first_name
            context['first_name'] = first_name
    elif request.method == "POST":
        if request.POST.get('auto_login') is not None:
            return redirect(reverse('videos'))
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        is_email = re.search("^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$", username_or_email)
        if is_email:
            try:
                user = User.objects.get(email = username_or_email)
                username = user.username
            except ObjectDoesNotExist:
                messages.error(request, "There is no account associated with that email.")
                return redirect(reverse("videos"))
            user = authenticate(request, username = username, password = password)
        else:
            user = authenticate(request, username = username_or_email, password = password)
        if user is not None:
            login(request, user)
            return redirect(reverse("videos"))
        else:
            messages.error(request, "Invalid username or password")
    context['logged_in'] = logged_in
    print(context)
    return render(request, "videos_interface/login.html", context)

def validate_username(username):
    if not username.isalnum():
        return {"username_invalid": "Username should only contain alphanumeric characters"}
    if User.objects.filter(username=username).exists():
        return {"username_invalid": "Username is not available"}
    if len(username) < 5 or len(username) > 10:
        return {"username_invalid": "Username should be between 3-8 characters"}
    return {"username_valid": True}

def validate_email(email):
    if not re.match(EMAIL_REGEX, email):
        return {"email_invalid": "Invalid email"}
    if User.objects.filter(email=email).exists():
        return {"email_invalid": "An account with this email is registered. Please login."}
    return {"email_valid": True}
    
def validate_create_account(request):
    response = {}
    data = json.loads(request.body)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    username_validation = validate_username(username)
    email_validation = validate_email(email)
    if username_validation.get('username_valid') and email_validation.get('email_valid'):
        # try:
            user = User.objects.create_user(username = username, email = email, password = password)
            login(request, user)
            # return redirect(reverse("videos"))
        # except IntegrityError:
        #     del username_validation['username_valid']
        #     username_validation['username_invalid'] = "An account with this information exists. Please login."
    response = dict(username_validation)
    response.update(email_validation)
    return JsonResponse(response)

def validate_login(request):
    data = json.loads(request.body)
    username_or_email = data.get('username_or_email')
    password = data.get('password')
    is_email = re.search("^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$", username_or_email)
    if is_email:
        try:
            user = User.objects.get(email = username_or_email)
            username = user.username
        except ObjectDoesNotExist:
            messages.error(request, "There is no account associated with that email.")
            return JsonResponse({'login_valid': False})
        user = authenticate(request, username = username, password = password)
    else:
        user = authenticate(request, username = username_or_email, password = password)
    if user is not None:
        login(request, user)
        # return redirect(reverse('videos'))
        return JsonResponse({'login_valid': True})
    else:
        messages.error(request, "Invalid username or password")
        return JsonResponse({'login_valid': False})


def logout_view(request):
    logout(request)
    return redirect(reverse("login"))

def create_account_view(request):
    # if request.method == "POST":
    #     first_name = request.POST.get('first_name')
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     email = request.POST.get('email')
    #     try:
    #         user = User.objects.create_user(first_name = first_name, username = username, email = email, password = password)
    #         login(request, user)
    #         return redirect(reverse("videos"))
    #     except IntegrityError:
    #         messages.error(request, "An account with this information exists. Please login.")
    return render(request, "videos_interface/create_account.html", {})

def videos(request):
    print("SESSIoN", request.session.items())
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
            print("YO")
            print("CLEANED", form.cleaned_data)
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
        



    


    

    
