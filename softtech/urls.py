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
from blogs.sitemaps import BlogSitemap
from news.sitemaps import NewsArticleSitemap
from django.contrib.sitemaps.views import sitemap
from softtech.sitemaps import StaticViewSitemap
from .views import download_video
from django.conf import settings
from django.conf.urls.static import static

sitemaps = {
    'blogs': BlogSitemap(),
    'news': NewsArticleSitemap(),
    'static': StaticViewSitemap(),
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about-us/',views.aboutUs),
    path('',views.homepage,name='myhomepage'),
    path('Blogs/',views.blog_page,name='blogs'),
    path('news/<slug:slug>/', views.article_detail, name='article_detail'),
    path('blogs/<slug:slug>/', views.blog_detail, name='blog_detail'), 
    path('contact/', views.contact, name='contact'),
    path('youtube-video-downloader/', views.download_video, name='download_video'),
    path('fetch-video-details/', views.fetch_video_details, name='fetch_video_details'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('youtube-video-downloader/', download_video, name='download_video'),
    path('youtube-video-downloader/<str:filename>/', views.download_video_file, name='download_video_file'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)