from django.contrib import admin
from .models import Video, Comment
from embed_video.admin import AdminVideoMixin


# Register your models here.\

class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(Video, MyModelAdmin)
admin.site.register(Comment)
