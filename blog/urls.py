from django.urls import path, re_path
from . import views

app_name = "blog"

urlpatterns = [
    path('article/', views.home, name="home"),
    path('', views.detail, name="detail")
]