from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ClientForm, ProductForm, ProductBuscarFormulario, TeacherForm
from .models import Client, Product, Teacher


def home(request):
    return render(request, "cliente/index.html")

def create_client(request):

    if request.method == 'POST':
        myForm = ClientForm(request.POST)

        if myForm.is_valid():
            data = myForm.cleaned_data
            profesor = Client(nombre=data["nombre"], apellido=data["apellido"], email=data["email"])
            profesor.save()

            return redirect("core:index")
        return render(request, "cliente/client_form.html", {"myForm": myForm})
    else:

        myForm = ClientForm()

        return render(request, "cliente/client_form.html", {"myForm": myForm})
    

    
def create_product(request):

    if request.method == 'POST':
        myForm = ProductForm(request.POST)

        if myForm.is_valid():
            data = myForm.cleaned_data
            product = Product(nombre=data["nombre"], precio=data["precio"])
            product.save()

            return redirect("core:index")
        return render(request, "cliente/product_form.html", {"myForm": myForm})
    else:

        myForm = ProductForm()

        return render(request, "cliente/product_form.html", {"myForm": myForm})
    

def create_teacher(request):

    if request.method == 'POST':
        myForm = TeacherForm(request.POST)

        if myForm.is_valid():
            data = myForm.cleaned_data
            profesor = Teacher(nombre=data["nombre"], apellido=data["apellido"], skill=data["skill"])
            profesor.save()

            return redirect("core:index")
        return render(request, "cliente/teacher_form.html", {"myForm": myForm})
    else:

        myForm = TeacherForm()

        return render(request, "cliente/teacher_form.html", {"myForm": myForm})



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
    teachers_all = []
    for teacher in Teacher.objects.all():
        teachers_all.append(teacher)

    context = {"teachers": teachers_all}
    return render(request, "cliente/teachers_view.html", context)
