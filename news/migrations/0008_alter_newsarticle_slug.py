# Generated by Django 5.1 on 2024-09-18 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_alter_newsarticle_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsarticle',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=255, unique=True),
        ),
    ]
