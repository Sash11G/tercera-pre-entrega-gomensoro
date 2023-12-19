from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


app_name = "cliente"

urlpatterns = [
    path('', views.home, name="index"),
    path('unauthorized/', views.unauthorized_access_view, name='unauthorized_access'),
     #### LOGIN ####
    path("registro", views.registro_view, name="registro"),
    path("login", views.login_view, name="login"),
    path("logout", LogoutView.as_view(template_name="cliente/logout.html"), name="logout"),
    #### BLOG ####
    path('create_blog_post/', views.create_blog_post, name='create-blog-post'),
    path('blogposts/', views.blog_post_list, name='blog-post-list'),
    #### EDITAR USUARIO ####
    path("editar-perfil", views.editar_perfil_view, name="editar-perfil"),
    path("create_avatar", views.crear_avatar_view, name="crear-avatar"),
    path('<int:user_id>/password/', views.change_password, name='change-password'),
    
]
    
    
    
