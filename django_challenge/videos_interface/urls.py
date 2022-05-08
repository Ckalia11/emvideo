from  django.urls  import  path
from . import  views

urlpatterns =[
path('', views.videos_interface, name= 'videos_interface'),
path('<int:pk>/', views.video_detail, name='video_detail'),
]