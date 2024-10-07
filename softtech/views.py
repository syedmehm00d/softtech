from django.http import HttpResponse
from django.shortcuts import render
from news.models import NewsArticle
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from blogs.models import Blog

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