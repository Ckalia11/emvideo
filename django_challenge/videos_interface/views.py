import re
from django.http import HttpResponse
from django.shortcuts import render
from .models import Video
from .forms import CommentForm

# Create your views here.

def videos_interface(request):
    objs = Video.objects.all()
    return render(request, 'videos_interface/videos_interface.html', {'objs': objs})

def video_detail(request, pk):
    obj = Video.objects.get(pk=pk)
    objs = Video.objects.all()
    if request.method == 'GET':
        form = CommentForm()
    elif request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            v = Video.objects.filter(pk=pk).update(comment=form.cleaned_data['comment'])
            HttpResponse("Your comment has been saved.")
        else:
            print(form.errors)
    return render(request, 'videos_interface/video.html', {'obj': obj, 'form':form, 'objs': objs})

    
