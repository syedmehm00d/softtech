from django.contrib import admin
from .models import Blog, BlogContent

class BlogContentInline(admin.TabularInline):
    model = BlogContent
    extra = 1

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogContentInline]
# Register your models here.
