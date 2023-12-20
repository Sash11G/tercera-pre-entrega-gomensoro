## SIGNALS UPDATE ##



## END SIGNALS UPDATE##
















from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BlogPostForm
from .models import BlogPost
from accounts.models import Avatar
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from PIL import Image



from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib import messages
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver




# User authentication



def home(request):
    return render(request, "cliente/index.html")

def render_form(request, form, template_name):
    return render(request, template_name, {"myForm": form})



  









def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            # Access form fields using cleaned_data and store in data
            data = form.cleaned_data
            new_blog_post = BlogPost(titulo=data["titulo"], contenido=data["contenido"], post_image=data["post_image"])

            new_blog_post = form.save(commit=False)
            new_blog_post.autor = request.user
            new_blog_post.avatar = Avatar.objects.filter(user=request.user).last()

            new_blog_post.save()

            return redirect('cliente:blog-post-list')  
    else:
        form = BlogPostForm()

    return render(request, 'cliente/blogpost_form.html', {'form': form})

# def blog_post_list(request):
#     blogposts = BlogPost.objects.all()[::-1]
#     context = {"blogposts": blogposts, "media_root": settings.MEDIA_ROOT}
#     return render(request, 'cliente/blogpost_list.html', context)


def blog_post_list(request):
    blogposts = BlogPost.objects.all()[::-1]

    # Fetch the latest avatar information for each post's author
    avatar_info = {}
    for post in blogposts:
        author = post.autor
        latest_avatar = Avatar.objects.filter(user=author).last()
        avatar_info[author.id] = latest_avatar

    return render(request, 'cliente/blogpost_list.html', {'blogposts': blogposts, 'avatar_info': avatar_info})

# solving if not blogspost ##



# # def create_blog_post(request):
# #     if request.method == 'POST':
# #         form = BlogPostForm(request.POST, request.FILES)
# #         if form.is_valid():
# #             # Access form fields using cleaned_data and store in data
# #             data = form.cleaned_data
# #             new_blog_post = BlogPost(titulo=data["titulo"], contenido=data["contenido"], post_image=data["post_image"])

# #             new_blog_post = form.save(commit=False)
# #             new_blog_post.autor = request.user
# #             new_blog_post.avatar = Avatar.objects.filter(user=request.user).last()
            

# #             new_blog_post.save()

# #             return redirect('cliente:blog-post-list')  
# #     else:
# #         form = BlogPostForm()

# #     return render(request, 'cliente/blogpost_form.html', {'form': form})

# # def blog_post_list(request):
    
# #     blogposts = BlogPost.objects.all()[::-1]
    
    
# #     context = {"blogposts": blogposts, "media_root": settings.MEDIA_ROOT}
# #     return render(request, 'cliente/blogpost_list.html', context)
