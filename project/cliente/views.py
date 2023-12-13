from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ClientForm, ProductForm, ProductBuscarFormulario, TeacherForm
from .models import Client, Product, Teacher
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.conf import settings


def home(request):
    return render(request, "cliente/index.html")

def render_form(request, form, template_name):
    return render(request, template_name, {"myForm": form})

def create_client(request):

    if request.method == 'POST':
        myForm = ClientForm(request.POST)

        if myForm.is_valid():
            data = myForm.cleaned_data
            client = Client(nombre=data["nombre"], apellido=data["apellido"], email=data["email"])
            client.save()

            return redirect("core:index")
        else:
            return render_form(request, myForm, "cliente/client_form.html")
    else:
        myForm = ClientForm()
        return render_form(request, myForm, "cliente/client_form.html")
    

    
def create_product(request):

    if request.method == 'POST':
        myForm = ProductForm(request.POST)

        if myForm.is_valid():
            data = myForm.cleaned_data
            product = Product(nombre=data["nombre"], precio=data["precio"])
            product.save()

            return redirect("core:index")

    
        else:
            return render_form(request, myForm, "cliente/product_form.html")
    else:
        myForm = ClientForm()
        return render_form(request, myForm, "cliente/product_form.html")
    

def create_teacher(request):

    if request.method == 'POST':
        myForm = TeacherForm(request.POST, request.FILES)

        if myForm.is_valid():
            data = myForm.cleaned_data

            teacher = Teacher(nombre=data["nombre"], apellido=data["apellido"], skill=data["skill"], foto_perfil=data["foto_perfil"])
            teacher.save()

            return redirect("cliente:view-teacher")

    
        else:
            return render_form(request, myForm, "cliente/teacher_form.html")
    else:
        myForm = TeacherForm()
        return render_form(request, myForm, "cliente/teacher_form.html")
    

class DeleteTeacher(DeleteView):
    model = Teacher
    template_name = 'cliente/teacher_confirm_delete.html'  # HTML template for delete confirmation
    context_object_name = 'object'

    success_url = reverse_lazy('cliente:view-teacher')  # Redirect to the list view after deletion

    def delete(self, request, *args, **kwargs):
        print("Delete method called")
        response = super().delete(request, *args, **kwargs)
        return response



def search_product(request):
    if request.method == "GET":
        form = ProductBuscarFormulario()
        return render(
            request,
            "cliente/product_search.html",
            context={"form": form}
        )
    else:
        formulario = ProductBuscarFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            filtered_products = []
            for product in Product.objects.filter(nombre__icontains=informacion["product"]):
                filtered_products.append(product)
            contexto = {"products": filtered_products}
            return render(request, "cliente/product_results.html", contexto)
        else:
            # Handle the case when the form is not valid
            # You might want to add some error messages or additional logic here
            return render(request, "cliente/product_search.html", context={"form": formulario})


def display_search_results(request):
    if request.method == "GET":
       
        search_query = request.GET.get('product', '')
        
       
        filtered_products = Product.objects.filter(nombre__icontains=search_query)

        
        context = {"products": filtered_products, "search_query": search_query}
        return render(request, "cliente/product_results.html", context)
    else:
        
        return HttpResponse("Method not allowed", status=405)
    
def view_teacher(request):
    teachers_all = Teacher.objects.all()

    context = {"teachers": teachers_all, "media_root": settings.MEDIA_ROOT}
    return render(request, "cliente/teachers_view.html", context)





##### LOGIN #####

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

def login_view(request):

    if request.user.is_authenticated:
        return render(
            request,
            "core/inicio.html",
            {"Message:": f"Welcome {request.user.username}!"}
        )

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
                {"Message": f"Welcome {modelo.username}"}
            )
        else:
            return render(
                request,
                "core/login.html",
                {"form": formulario}
            )


def logout_view(request):
    pass



from .forms import UserCreationFormulario, UserEditionFormulario
from django.contrib.auth.views import PasswordChangeView

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