from django.contrib.auth import views
from django.urls import path
from .views import home, ArticleList

app_name = 'account'
urlpattern = [
    path('login/', views.LoginView.as_view(), name= 'login'),
]

urlpattern += [
    path('', ArticleList.as_view(), name= 'home')
]