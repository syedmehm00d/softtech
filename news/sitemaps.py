from django.contrib.sitemaps import Sitemap
from .models import NewsArticle  # Import your NewsArticle model

class NewsArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return NewsArticle.objects.all()

    def lastmod(self, obj):
        return obj.news_datetime_published  # Ensure this field reflects the last modification date
