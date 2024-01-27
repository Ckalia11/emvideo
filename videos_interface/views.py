from xml.dom import ValidationErr
from django.shortcuts import redirect, render
from .models import Channel, Video, Comment, Thumbnail
from .forms import CommentForm, VideoForm, VideoSearchForm
import os
import cv2
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
import regex as re
from django.http import JsonResponse
import json
from django.core.files.base import ContentFile
from emvideo.settings import MEDIA_URL

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


def root_view(request):
    return redirect("login")

# get profile pic/channel


def get_user_profile(request):
    profile_picture = None
    if request.user.is_authenticated:
        try:
            user = User.objects.get(pk=request.user.pk)
            try:
                channel = Channel.objects.get(user=user)
                if channel.image:
                    profile_picture = channel.image
                else:
                    profile_picture = "images/profile/default.png"
            except Channel.DoesNotExist:
                raise ValidationErr("Channel does not exist")
        except User.DoesNotExist:
            raise ValidationErr("User does not exist")
    return user


def videos(request):
    # search_query = request.session.get('search_query')
    # Remove the search query from the session
    # if search_query:
    #     del request.session['search_query']
    #     request.session.modified = True
    #     thumbnails = Thumbnail.objects.filter(video__title__startswith=search_query)
    # else:
    # Thumbnail.objects.all()
    # search_form = VideoSearchForm()
    # context = {"thumbnails": thumbnails,
    #            "search_query": search_query, 'search_form': search_form}
    # if Video.objects.count() == 0:
    #     context['message'] = "There are no videos."
    return render(request, 'videos_interface/videos.html', {})


def video_search(request, filter_account_videos):
    search_form = VideoSearchForm(request.GET)
    if search_form.is_valid():
        search_query = search_form.cleaned_data['search_query']
        request.session['search_query'] = search_query
        request.session.modified = True
    else:
        search_query = None
    query_paramater = f'?query={search_query}' if search_query else ""
    if filter_account_videos:
        return redirect(reverse('my_videos') + query_paramater)
    else:
        return redirect(reverse('videos') + query_paramater)


def create_thumbnail(video):
    video_path = os.path.join(MEDIA_URL, str(video.videofile))
    vidcap = cv2.VideoCapture(video_path)
    # capture thumbnail at 1 second mark
    vidcap.set(cv2.CAP_PROP_POS_MSEC, 1000)
    success, array = vidcap.read()
    if success:
        thumbnail_name = f"thumbnail_for_video_{video.pk}.jpg"
        frame_jpg = cv2.imencode('.jpg', array)
        # get bytes array from tuple
        file = ContentFile(frame_jpg[1])
        t = Thumbnail(video=video)
        t.image_file.save(thumbnail_name, file)


def my_videos(request):
    if request.user.is_authenticated:
        search_query = request.session.get('search_query')
        thumbnails = Thumbnail.objects.filter(video__user=request.user)
        if search_query:
            del request.session['search_query']
            request.session.modified = True
            thumbnails = thumbnails.filter(
                video__title__startswith=search_query)
        search_form = VideoSearchForm()
        context = {"thumbnails": thumbnails,
                   "search_query": search_query, 'search_form': search_form}
        videos_count = Video.objects.filter(user=request.user).count()
        if videos_count == 0:
            context['message'] = "You haven't uploaded any videos."
    return render(request, 'videos_interface/my_videos.html', context)


def create_video(request):
    if request.method == "GET":
        form = VideoForm()
    elif request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            videofile = form.cleaned_data.get("videofile")
            video = Video.objects.create(
                title=title, videofile=videofile, user=request.user)
            create_thumbnail(video)
            return redirect(reverse("my_videos"))
    context = {
        'form': form
    }
    return render(request, 'videos_interface/create_video.html', context)


def video_detail(request, pk):
    video = Video.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            Comment.objects.create(
                comment=comment, user=request.user, video=video)
            # messages.success(request, "Comment was saved.")
            return redirect(reverse('video_detail', kwargs={"pk": pk}))
    elif request.method == 'GET':
        form = CommentForm()
        comments = Comment.objects.filter(video__pk=pk)
    context = {'video': video, 'form': form, 'comments': comments}
    return render(request, 'videos_interface/video.html', context)


def my_video_detail(request, pk):
    video = Video.objects.get(pk=pk)
    context = {'video': video}
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


def my_video_delete(request, pk):
    # deletes video instance, thumbnail instance, and thumbnail file on server
    Video.objects.get(pk=pk).delete()
    return redirect(reverse('my_videos'))

# def _add_click(request):
#     if Clicks.objects.filter(user=request.user,video=video).exists():
#         click = Clicks.objects.get(user=request.user,video=video)
#         click.clicks = click.clicks + 1
#         click.save()
#     else:
#         click = Clicks.objects.create(user=request.user,video=video,clicks=1)


def validate_login(request):
    data = json.loads(request.body)
    username_or_email = data.get('username_or_email')
    password = data.get('password')
    is_email = re.search(
        "^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$", username_or_email)
    if is_email:
        try:
            user = User.objects.get(email=username_or_email)
            username = user.username
        except ObjectDoesNotExist:
            return JsonResponse({'login_valid': False})
        user = authenticate(request, username=username, password=password)
    else:
        user = authenticate(
            request, username=username_or_email, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'login_valid': True})
    else:
        return JsonResponse({'login_valid': False})


def validate_create_account(request):
    response = {}
    data = json.loads(request.body)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    username_validation = validate_username_create(username)
    email_validation = validate_email_create(email)
    if username_validation.get('username_valid') and email_validation.get('email_valid'):
        user = User.objects.create_user(
            username=username, email=email, password=password)
        channel = Channel.objects.create(user=user)
        login(request, user)
        messages.info(request, 'Account was created successfully')
    response = dict(username_validation)
    response.update(email_validation)
    return JsonResponse(response)


def validate_username_create(username):
    if not username.isalnum():
        return {"username_invalid": "Username should only contain alphanumeric characters"}
    if User.objects.filter(username=username).exists():
        return {"username_invalid": "Username is not available"}
    if len(username) < 3 or len(username) > 8:
        return {"username_invalid": "Username should be between 3-8 characters"}
    return {"username_valid": True}


def validate_email_create(email):
    if not re.match(EMAIL_REGEX, email):
        return {"email_invalid": "Invalid email"}
    if User.objects.filter(email=email).exists():
        return {"email_invalid": "An account with this email is registered. Please login."}
    return {"email_valid": True}


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('videos'))
    return render(request, "videos_interface/login.html")
