from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User



def acceder(request):
    error_type = ""
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect("home")
            else:
                # Contraseña incorrecta
                error_type = "password"
        else:
            # Verifica si el usuario no existe
            nombre_usuario = request.POST.get("username")
            if not User.objects.filter(username=nombre_usuario).exists():
                error_type = "user"
            else:
                error_type = "password"  # O puedes usar 'invalid' si quieres diferenciar
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {
        "form": form,
        "error_type": error_type
    })



def homePage(request):
    return render(request, "bienvenido.html", {})

def salir(request):
    logout(request)
    messages.info(request, "Saliste exitosamente")
    return redirect("login")

