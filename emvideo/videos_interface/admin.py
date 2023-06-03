from django.contrib import admin
from .models import Video, Comment, Thumbnail
from embed_video.admin import AdminVideoMixin


# Register your models here.\

class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

class VideoAdmin(admin.ModelAdmin):
    readonly_fields=('id',)

class ThumbnailAdmin(admin.ModelAdmin):
    readonly_fields=('id',)

class CommentAdmin(admin.ModelAdmin):
    readonly_fields=('id',)

admin.site.register(Video, VideoAdmin)
admin.site.register(Thumbnail, ThumbnailAdmin)
admin.site.register(Comment, CommentAdmin)

