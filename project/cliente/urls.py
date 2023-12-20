from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


app_name = "cliente"

urlpatterns = [
    path('', views.home, name="index"),
    #### BLOG ####
    path('create_blog_post/', views.create_blog_post, name='create-blog-post'),
    path('blogposts/', views.blog_post_list, name='blog-post-list'),
    
]
    
    
    
