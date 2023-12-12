from django.urls import path
from . import views


app_name = "cliente"

urlpatterns = [
    path('', views.home, name="index"),
    path('create_client/', views.create_client, name="create-user"),
    path('create_product/', views.create_product, name="create-product"),
    path('search_product/', views.search_product, name="search-product"),
    path('search_results/', views.display_search_results, name='search-results'),
    path('create_teacher/', views.create_teacher, name='create-teacher'),
    path('view_teacher/', views.view_teacher, name='view-teacher'),
    path('teacher/<int:pk>/delete/', views.DeleteTeacher.as_view(), name='delete-teacher'),
    
    
    
    
]
