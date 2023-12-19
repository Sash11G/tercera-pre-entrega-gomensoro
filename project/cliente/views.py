from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BlogPostForm, UserCreationFormulario, UserAvatarFormulario, UserEditionFormulario
from .models import BlogPost, Avatar
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from PIL import Image



from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User


# User authentication
def is_admin(user):
    return user.is_authenticated and user.is_superuser

def unauthorized_access_view(request):
    print("Unauthorized Access View Called")
    return render(request, 'cliente/unauthorized_access.html')

def home(request):
    return render(request, "cliente/index.html")

def render_form(request, form, template_name):
    return render(request, template_name, {"myForm": form})



  


##### LOGIN #####
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

@user_passes_test(lambda user: not user.is_authenticated, login_url='core:index')
def login_view(request):

    if request.user.is_authenticated:
        message = f"Welcome {request.user.username}!"
        return render(request, "core/inicio.html", {"message": message})


    if request.method == "GET":
        return render(
            request,
            "cliente/login.html",
            {"form": AuthenticationForm()}
        )
    else:
        formulario = AuthenticationForm(request, data=request.POST)

        if formulario.is_valid():
            informacion = formulario.cleaned_data
            usuario = informacion["username"]
            password = informacion["password"]

            modelo = authenticate(username=usuario, password=password)
            login(request, modelo)

            return render(
                request,
                "core/inicio.html",
                {"message": f"Welcome {modelo.username}"}
            )
        else:
            return render(
                request,
                "cliente/login.html",
                {"form": formulario}
            )


def logout_view(request):
    pass





@user_passes_test(lambda user: not user.is_authenticated, login_url='core:index')
def registro_view(request):

    if request.method == "GET":
        return render(
            request,
            "cliente/registro.html",
            {"form": UserCreationFormulario()}
        )
    else:
        formulario = UserCreationFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            user = informacion["username"]
            formulario.save()

            return render(
                request,
                "core/inicio.html",
                {"Message": f"User created: {user}"}
            )
        else:
            return render(
                request,
                "cliente/registro.html",
                {"form": formulario}
            )
        

#### BLOG ####




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

def blog_post_list(request):
    
    blogposts = BlogPost.objects.all()
    
    context = {"blogposts": blogposts, "media_root": settings.MEDIA_ROOT}
    return render(request, 'cliente/blogpost_list.html', context)



# @login_required
# def editar_perfil_view(request):
#     usuario = request.user
#     avatar = Avatar.objects.filter(user=usuario).last()
#     avatar_url = avatar.imagen.url if avatar is not None else ""

#     if request.method == "GET":
#         formulario = UserEditionFormulario(instance=usuario)
#         return render(
#             request,
#             "cliente/editar_perfil.html",
#             context={"form": formulario, "usuario": usuario, "avatar_url": avatar_url}
#         )
#     else:
#         formulario = UserEditionFormulario(request.POST, instance=usuario)
#         if formulario.is_valid():
#             informacion = formulario.cleaned_data

#             usuario.email = informacion["email"]
#             usuario.first_name = informacion["first_name"]
#             usuario.last_name = informacion["last_name"]

#             # Update the password using set_password
#             password = informacion.get("password1")
#             if password:
#                 usuario.set_password(password)

#             usuario.save()
#             return redirect("core:index")

#         return render(
#             request,
#             "cliente/editar_perfil.html",
#             context={"form": formulario, "usuario": usuario, "avatar_url": avatar_url}
#         )
    

@login_required
def editar_perfil_view(request):
    usuario = request.user
    avatar = Avatar.objects.filter(user=usuario).last()
    avatar_url = avatar.imagen.url if avatar is not None else ""

    if request.method == "GET":
        avatar_form = UserAvatarFormulario()
        profile_form = UserEditionFormulario(instance=usuario)
    elif request.method == "POST":
        avatar_form = UserAvatarFormulario(request.POST, request.FILES)
        profile_form = UserEditionFormulario(request.POST, instance=usuario)

        # Check if either avatar form or profile form is valid
        if avatar_form.is_valid() or profile_form.is_valid():
            # Update the avatar if an image is provided and there is an existing avatar
            avatar_info = avatar_form.cleaned_data
            if avatar_info.get("imagen"):
                if avatar:
                    # Update the existing avatar
                    avatar.imagen = avatar_info["imagen"]
                else:
                    # Create a new avatar if there was no previous avatar
                    avatar = Avatar(user=usuario, imagen=avatar_info["imagen"])

                # Resize the avatar image to your desired dimensions

                # Save the avatar
                avatar.save()

            # Save the profile details if they are not empty
            if profile_form.is_valid():
                profile_info = profile_form.cleaned_data
                if profile_info.get("email"):
                    usuario.email = profile_info["email"]
                if profile_info.get("first_name"):
                    usuario.first_name = profile_info["first_name"]
                if profile_info.get("last_name"):
                    usuario.last_name = profile_info["last_name"]

                # Update the password using set_password
                password = profile_info.get("password1")
                if password:
                    usuario.set_password(password)

                usuario.save()
                return redirect("core:index")

    # Handle invalid form submissions
    return render(
        request,
        "cliente/editar_perfil.html",
        context={"avatar_form": avatar_form, "profile_form": profile_form, "usuario": usuario, "avatar_url": avatar_url}
    )




def change_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update the session with the new password
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password_success')  # Redirect to a success page
    else:
        form = PasswordChangeForm(user)

    return render(request, 'cliente/change_password.html', {'form': form, 'user': user})



@login_required
def crear_avatar_view(request):

    usuario = request.user

    if request.method == "GET":
        formulario = UserAvatarFormulario()
        return render(
            request,
            "cliente/crear_avatar.html",
            context={"form": formulario, "usuario": usuario}
        )
    else:
        formulario = UserAvatarFormulario(request.POST, request.FILES)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            modelo = Avatar(user=usuario, imagen=informacion["imagen"])
            modelo.save()
            return redirect("core:index")