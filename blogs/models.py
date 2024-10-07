import os
import uuid
from django.db import models
from tinymce.models import HTMLField
from django.utils.text import slugify

def unique_image_path(instance, filename):
    # Get the file extension of the uploaded file
    ext = filename.split('.')[-1]
    # Generate a new filename using a UUID
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return the full path where the image will be stored
    return os.path.join('blog_images/', new_filename)

class Blog(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=255, blank=True, editable=False)
    description = models.TextField(default="Default description")
    # Use the custom path function for the image field
    image = models.ImageField(upload_to=unique_image_path)
    published_date =  models.DateTimeField()

    def save(self, *args, **kwargs):
        # Only generate slug if it doesn't already exist
        if not self.slug:
            # Create the initial slug
            original_slug = slugify(self.title)
            unique_slug = original_slug
            number = 1

            # Ensure the slug is unique
            while Blog.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{original_slug}-{number}'
                number += 1

            # Set the unique slug
            self.slug = unique_slug
        
        super().save(*args, **kwargs)


class BlogContent(models.Model):
    BLOG_CONTENT_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image')
    ]
    
    blog = models.ForeignKey(Blog, related_name='contents', on_delete=models.CASCADE)
    content_type = models.CharField(max_length=5, choices=BLOG_CONTENT_TYPE_CHOICES)
    text = HTMLField(blank=True, null=True)  # Use TinyMCE for rich text (subheadings)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField()  # This defines the order of content

    class Meta:
        ordering = ['order']
# Create your models here.
