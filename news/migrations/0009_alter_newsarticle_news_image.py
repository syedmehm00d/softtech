# Generated by Django 5.1 on 2024-09-18 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_alter_newsarticle_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsarticle',
            name='news_image',
            field=models.ImageField(upload_to='static/images/articles/'),
        ),
    ]
