from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from cliente.forms import BlogPostForm
from cliente.models import BlogPost
from .forms import UserCreationFormulario, UserAvatarFormulario, UserEditionFormulario, CustomPasswordChangeForm
from .models import Avatar
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test, login_required
from PIL import Image

from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash, login, authenticate

from django.contrib import messages
from django.contrib.auth.models import User
import logging






# Create your views here.

def is_admin(user):
    return user.is_authenticated and user.is_superuser

def unauthorized_access_view(request):
    print("Unauthorized Access View Called")
    return render(request, 'account/unauthorized_access.html')




logger = logging.getLogger(__name__)
@user_passes_test(lambda user: not user.is_authenticated, login_url='core:index')
def login_view(request):

    if request.user.is_authenticated:
        message = f"Welcome {request.user.username}!"
        return render(request, "core/inicio.html", {"message": message})


    if request.method == "GET":
        return render(
            request,
            "accounts/login.html",
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
                "accounts/login.html",
                {"form": formulario}
            )
        

def logout_view(request):
    pass



@user_passes_test(lambda user: not user.is_authenticated, login_url='core:index')
def registro_view(request):

    if request.method == "GET":
        return render(
            request,
            "accounts/registro.html",
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
                "accounts/registro.html",
                {"form": formulario}
            )
        

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

    return render(request, 'accounts/change_password.html', {'form': form, 'user': user})


@login_required
def editar_perfil_view(request):
    usuario = request.user
    avatar = Avatar.objects.filter(user=usuario).last()
    avatar_url = avatar.imagen.url if avatar is not None else ""

    if request.method == "GET":
        avatar_form = UserAvatarFormulario()
        profile_form = UserEditionFormulario(instance=usuario)
        password_form = CustomPasswordChangeForm(user=usuario)  # Pass the user instance to the password form
    elif request.method == "POST":
        avatar_form = UserAvatarFormulario(request.POST, request.FILES)
        profile_form = UserEditionFormulario(request.POST, instance=usuario)
        password_form = CustomPasswordChangeForm(user=usuario, data=request.POST)

        # Check if all forms are valid
        if all([avatar_form.is_valid(), profile_form.is_valid(), password_form.is_valid()]):
            # Update the avatar if an image is provided
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
            profile_info = profile_form.cleaned_data
            if profile_info.get("email"):
                usuario.email = profile_info["email"]
            if profile_info.get("first_name"):
                usuario.first_name = profile_info["first_name"]
            if profile_info.get("last_name"):
                usuario.last_name = profile_info["last_name"]

            # Update the password if the password form is valid
            password_info = password_form.cleaned_data
            if password_info.get("new_password1"):
                # Save the form to change the password
                password_form.save()

                # Update session to keep the user logged in after password change
                update_session_auth_hash(request, usuario)

            usuario.save()
            return redirect("core:index")

    return render(
        request,
        "accounts/editar_perfil.html",
        {"avatar_form": avatar_form, "profile_form": profile_form, "password_form": password_form, "avatar": avatar},
    )