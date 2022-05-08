from django.db import models
from  embed_video.fields  import  EmbedVideoField
from django.contrib.postgres.fields import ArrayField


# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=200)
    comment = models.CharField(max_length=100, blank=True)
    video = EmbedVideoField()
