from django.db import models
# from  embed_video.fields  import  EmbedVideoField
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
# should have a user table

class Video(models.Model):
    title = models.CharField(max_length=200, blank=True)
    videofile= models.FileField(upload_to='videos/', blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    views = models.IntegerField(null=True, blank = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Video {self.pk}"

class Comment(models.Model):
    comment = models.CharField(max_length=100)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Comment {self.pk}"

class Thumbnail(models.Model):
    image_file = models.ImageField(upload_to = "images/thumbnails/")
    video = models.OneToOneField(
        Video,
        blank = True,
        null = True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Thumbnail {self.pk}"

class Channel(models.Model):
    image = models.ImageField(null = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)

 # class Clicks(models.Model):
#     clicks = models.IntegerField()
#     video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, related_name='click_video')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

#     class Meta:
#         verbose_name = 'Click'
#         verbose_name_plural = 'Clicks'

