from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Article, Category

# Create your views here.
def home(request):
    context = {
        "articles" : Article.objects.filter(status= 'p').order_by('publish'),
        "category" : Category.objects.filter(status= True)
    }
    return render(request, "blog/home.html", context)

def detail(request):
    context = {
        "article": Article.objects.all()
    }
    return render(request, "blog/detail.html", context)


