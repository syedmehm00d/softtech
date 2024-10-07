from django.contrib import admin
from news.models import NewsArticle

class NewsAdmin(admin.ModelAdmin):
    list_display = ('news_title', 'news_desc', 'news_image', 'news_datetime_published')  


admin.site.register(NewsArticle, NewsAdmin)
# Register your models here.
