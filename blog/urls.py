from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='all_blogs'),
    path('<int:blog_id>/', views.blog_detail, name='blog_detail'),
]
