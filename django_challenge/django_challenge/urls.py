from django.contrib.auth import views as auth_views

"""django_challenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy
from videos_interface import views
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('accounts/login/validate_login/', csrf_exempt(views.validate_login), name = 'validate_login'),
    path('accounts/create/', TemplateView.as_view(template_name = 'videos_interface/create_account.html'), name = 'create_account'),
    path('accounts/create/validate_create_account/', csrf_exempt(views.validate_create_account), name = 'validate_create_account'),
    path('accounts/create/validate_username_create/', csrf_exempt(views.validate_username_create), name = 'validate_username_create'),
    path('accounts/create/validate_email_create/', csrf_exempt(views.validate_email_create), name = 'validate_email_create'),
    path('accounts/logout', views.logout_view, name = 'logout'),
    path('accounts/profile', TemplateView.as_view(template_name = 'videos_interface/profile.html'), name = 'profile'),
    path('videos/', include('videos_interface.urls')), 
    
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)