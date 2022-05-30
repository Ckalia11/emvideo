from  django.urls  import  path
from . import  views

urlpatterns =[
path('', views.videos, name= 'videos'),
path('<int:pk>/', views.video_detail, name='video_detail'),
path('my_videos/', views.my_videos, name = "my_videos"),
path('create_video', views.create_video, name = "create_video"),
path('my_videos/<int:pk>', views.my_video_detail, name = "my_video_detail"),
path('my_videos/<int:pk>/edit', views.my_video_edit, name = "my_video_edit")
]