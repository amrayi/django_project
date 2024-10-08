from django.urls import path, re_path
from .views import ArticleList, ArticleDetail, CategoryList, AuthorList, ArticlePreview

app_name = "blog"

urlpatterns = [
    path('', ArticleList.as_view(), name="home"),
    path('page/<int:page>', ArticleList.as_view(), name="home"),
    path('article/<slug:slug>', ArticleDetail.as_view(), name="detail"),
    path('article/<int:spk>', ArticlePreview.as_view(), name="preview"),
    path('category/<slug:slug>', CategoryList.as_view() , name="category"),
    path('category/<slug:slug>/page/<int:page>', CategoryList.as_view(), name="category"),
    path('category/<slug:username>', AuthorList.as_view() , name="author"),
    path('category/<slug:username>/page/<int:page>', AuthorList.as_view(), name="author"),
]