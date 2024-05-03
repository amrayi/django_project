from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Article, Category

# Create your views here.
def home(request):
    context = {
        "articles" : Article.objects.published(),
        "category" : Category.objects.filter(status= True)
    }
    return render(request, "blog/home.html", context)

def detail(request, slug):
    context = {
        "article": get_object_or_404(Article.objects.published(), slug=slug),
        "category" : Category.objects.filter(status= True)
    }
    return render(request, "blog/detail.html", context)

def category(request, slug):
    context = {
        "category": get_object_or_404(Category.objects.published(), slug=slug)
    }
    return render(request, "blog/category.html", context)


