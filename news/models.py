import os
import uuid
from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField

def unique_image_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Create a new filename using UUID
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return the path where the image will be stored in the media directory
    return os.path.join('news_images/', new_filename)

class NewsArticle(models.Model):
     CATEGORY_CHOICES = [
        ('PAKISTAN', 'Pakistan'),
        ('BUSINESS', 'Business'),
        ('INTERNATIONAL', 'International'),
        ('SPORTS', 'Sports'),
    ]
     
     news_title = models.CharField(max_length=255)
     news_desc = HTMLField()
     news_detail = HTMLField() 
     news_image = models.ImageField(upload_to=unique_image_path)
     news_datetime_published = models.DateTimeField()
     category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
     slug = models.SlugField(unique=True, max_length=255, blank=True, editable=False)
     views = models.IntegerField(default=0)

     def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.news_title)
            slug = base_slug
            counter = 1
            while NewsArticle.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
# Create your models here.
