from django import forms
from .models import Video


class CommentForm(forms.Form):
    comment = forms.CharField(max_length=10)

class VideoForm(forms.ModelForm):
    class Meta:
        model= Video
        fields= ['title', 'videofile', 'clicks']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        print(title)

    def clean_videofile(self):
        pass




