from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blog-index'),
    path('blog/<slug:slug>/', views.blog, name='blog_detail'),
    path('category/<slug:slug>/', views.category_view, name='category_view'),
    path('search/', views.search_view, name='search'),
]