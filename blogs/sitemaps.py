from django.contrib.sitemaps import Sitemap
from .models import Blog  # Import your Blog model

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.published_date  # Replace with the actual field that stores last updated time
