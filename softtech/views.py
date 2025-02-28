from django.http import HttpResponse, JsonResponse,FileResponse
from news.models import NewsArticle
from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator
from blogs.models import Blog
from django import forms
import requests
from django.middleware.csrf import get_token
import os
import uuid
import yt_dlp
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .forms import YouTubeDownloadForm
import subprocess
import logging
logger = logging.getLogger(__name__)

def homepage(request):
    category = request.GET.get('category', 'ALL')  # Get the category from query parameters, default to 'ALL'
    if category == 'ALL':
        data_new = NewsArticle.objects.all().order_by('-news_datetime_published')
    else:
        data_new = NewsArticle.objects.filter(category=category).order_by('-news_datetime_published')
    
    paginator = Paginator(data_new, 6)  # Show 10 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    newsData = {
        'page_obj': page_obj,
        'selected_category': category,
    }
    return render(request, "Default.html", newsData)

def article_detail(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug)
     # Increment the view count
    article.views += 1
    article.save()
    return render(request, 'article_detail.html', {'article': article})

def aboutUs(request):
   return HttpResponse("Welcome to Business Management Solution")

def blog_page(request):
    blogs = Blog.objects.all()  # Fetch all blog entries
    return render(request, 'Blogs.html', {'blogs': blogs})

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    contents = blog.contents.all()  # Assuming you're using a BlogContent model for content sections
    return render(request, 'blog_detail.html', {'blog': blog, 'contents': contents})

def blog_list(request):
    # Fetch all blog entries
    blogs = Blog.objects.all()
    # Pass the blogs to the context
    return render(request, 'your_template.html', {'blogs': blogs})

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)

DISCORD_WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1333831661695270943/vKnVfqAflp-JgkxJnQXnwuuRNDDQFJobmtopKBFJ06-bk9gGAyVfhVOWB92LgNVFZTcz'

def contact(request):
    if request.method == 'POST':

        print("CSRF Token (expected by Django):", get_token(request))
        # Initialize the form with POST data
        form = ContactForm(request.POST)
        
        if form.is_valid():  # Validate the form data
            # Get cleaned data from the form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Prepare the message for Discord
            discord_message = (
                f"**New Contact Form Fresh Insights_Blogs**\n"
                f"**Name**: {name}\n"
                f"**Email**: {email}\n"
                f"**Subject**: {subject}\n"
                f"**Message**: {message}"
            )

            # Send the message to Discord
            response = requests.post(DISCORD_WEBHOOK_URL, json={"content": discord_message})

            # Check if the request to Discord was successful
            if response.status_code == 204:  # HTTP 204 No Content
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Failed to send message to Discord'}, status=500)

        # If the form is not valid, return an error response
        return JsonResponse({'success': False, 'error': 'Invalid form data'}, status=400)

    # If the request is GET, render the contact form
    form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def download_video(request):
    form = YouTubeDownloadForm()

    if request.method == 'POST':
        form = YouTubeDownloadForm(request.POST)

        if form.is_valid():
            youtube_url = form.cleaned_data['youtube_url']
            logger.debug("Selected YouTube URL: %s", youtube_url)

            try:
                # Generate a unique filename
                unique_filename = str(uuid.uuid4())  
                download_folder = os.path.join(settings.MEDIA_ROOT)  # Save to MEDIA_ROOT
                os.makedirs(download_folder, exist_ok=True)  # Ensure folder exists
                download_path = os.path.join(download_folder, f"{unique_filename}.mp4")

                # Download the best video in MP4 format using yt-dlp
                download_command = [
                    'yt-dlp', '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4', 
                    youtube_url, 
                    '-o', download_path
                ]
                subprocess.run(download_command, check=True)

                # Check if the file exists
                if os.path.exists(download_path):
                    logger.info(f"File downloaded successfully: {download_path}")
                    download_link = f"/media/{unique_filename}.mp4"  # Serve via media URL
                    
                    # Send the download link back to the frontend
                    return JsonResponse({"success": True, "download_link": download_link})
                else:
                    logger.error("MP4 file not found after download.")
                    return JsonResponse({"error": "File not found after download."}, status=500)

            except subprocess.CalledProcessError as e:
                logger.error("Error during video download: %s", str(e))
                return JsonResponse({"error": "An error occurred while processing the video download."}, status=500)

    return render(request, 'download_video.html', {'form': form})

def download_video_file(request, filename):
    # Construct the file path
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    # Check if file exists
    if os.path.exists(file_path):
        # Open the file in binary mode
        with open(file_path, 'rb') as video_file:
            response = FileResponse(video_file, content_type='video/mp4')
            
            # Force the browser to download the file
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return JsonResponse({"error": "File not found."}, status=404)

@csrf_exempt
def fetch_video_details(request):
    if request.method == "POST":
        youtube_url = request.POST.get("youtube_url")

        try:
            ydl_opts = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=False)

            video_title = info.get("title", "Unknown Title")
            video_thumbnail = info.get("thumbnail", info.get("thumbnails", [{}])[-1].get("url", ""))

            qualities = [
                {"format_id": f["format_id"], "format_note": f"{f['resolution']} - {f['ext']}"}
                for f in info["formats"]
                if f.get("resolution")
            ]

            return JsonResponse({
                "success": True,
                "title": video_title,
                "thumbnail": video_thumbnail,
                "qualities": qualities
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})