from typing import Any
from account.models import User
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from account.mixins import AuthorAccessMixin
# from django.http import HttpResponse, JsonResponse
from .models import Article, Category

# Create your views here.
def home(request, page =1):
    article_list = Article.objects.published()
    paginator = Paginator(article_list, 6)
    articles = paginator.get_page(page)
    context = {
        "articles" : articles,
        "category" : Category.objects.filter(status= True)
    }
    return render(request, "blog/home.html", context)
class ArticleList(ListView):
    queryset = Article.objects.published()
    paginate_by = 6
    

# def detail(request, slug):
#     context = {
#         "article": get_object_or_404(Article.objects.published(), slug=slug),
#         "category" : Category.objects.filter(status= True)
#     }
#     return render(request, "blog/detail.html", context)
class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article.objects.published(), slug=slug)
#     return render(request, "blog/detail.html", context)

class ArticlePreview(AuthorAccessMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk =pk)


# def category(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, status=True)
#     article_list = category.articles.published()
#     paginator = Paginator(article_list, 6)
#     articles = paginator.get_page(page)
#     context = {
#         "category": category,
#         "article" : articles
#     }
#     return render(request, "blog/category.html", context)
class CategoryList(ListView):
    paginate_by = 6
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class AuthorList(ListView):
    paginate_by = 6
    template_name = 'blog/auther_list.html'

    def get_queryset(self):
        global author
        username = self.kwargs.get('slug')
        author = get_object_or_404(User.objects.active(), username=username)
        return author.articles.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context