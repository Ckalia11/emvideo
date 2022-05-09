from django.db import models
from  embed_video.fields  import  EmbedVideoField
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
# should have a user table

class Video(models.Model):
    title = models.CharField(max_length=200)
    video = EmbedVideoField()


class Comment(models.Model):
    comment = models.CharField(max_length=100)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, to_field='id')

