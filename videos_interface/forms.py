from django import forms
from .models import Video
from django.forms import ModelForm, ValidationError
import os

class VideoSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search videos'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["search_query"].widget.attrs['class'] = 'form-control mr-sm-2 btn-lg'

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




