from django import forms
from .models import Video
from django.forms import ModelForm, ValidationError
import os


class CommentForm(forms.Form):
    comment = forms.CharField(max_length=10)

class VideoForm(forms.ModelForm):
    class Meta:
        model= Video
        fields= ['title', 'videofile']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Video Title'}),
            'videofile': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

        labels = {
        "title": "Title",
    }


    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError('Please enter a title')
        if len(title) > 30:
            raise ValidationError('Title is too long')
        return title

    def clean_videofile(self):
        allowed_file_extensions = ('.mp4')
        videofile = self.cleaned_data.get('videofile')
        if not videofile:
            raise ValidationError('Please select a video file')
        name, ext = os.path.splitext(videofile.name)
        if ext not in allowed_file_extensions:
            raise ValidationError('File must be of type .mp4')
        return videofile


    


    # def clean_videofile(self):
    #     pass




