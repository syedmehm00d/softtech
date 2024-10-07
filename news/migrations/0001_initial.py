# Generated by Django 5.1 on 2024-08-30 18:21

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_title', models.CharField(max_length=255)),
                ('news_desc', tinymce.models.HTMLField()),
                ('news_image', models.ImageField(upload_to='news_images/')),
                ('news_datetime_published', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
