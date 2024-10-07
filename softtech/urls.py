"""
URL configuration for softtech project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from softtech import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about-us/',views.aboutUs),
    path('',views.homepage,name='myhomepage'),
    path('Blogs/',views.blog_page,name='blogs'),
    path('news/<slug:slug>/', views.article_detail, name='article_detail'),
    path('blogs/<slug:slug>/', views.blog_detail, name='blog_detail'), 
]
