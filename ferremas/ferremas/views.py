from django.shortcuts import render, redirect
import requests

def index(request):
    return render(request, 'index.html')


# Vista para la página "About"
def about(request):
    return render(request, 'about.html')


# Vista para la página "Cart"
def cart(request):
    return render(request, 'cart.html')

# Vista para la página "Contact"
def contact(request):
    return render(request, 'contact.html')

def shop(request):
    return render(request, 'shop.html')

def single_product(request):
    return render(request, 'single-product.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # Cambia el puerto si tu API está en otro
        response = requests.post(
            "http://127.0.0.1:8001/login/",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            request.session["username"] = data["username"]
            request.session["rol"] = data["rol"]
            return redirect("index")
        else:
            return render(request, "login.html", {"form": {"errors": True}})
    return render(request, "login.html", {"form": {}})

def registro_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 != password2:
            return render(request, "registro.html", {"form": {"errors": True}})
        response = requests.post(
            "http://127.0.0.1:8001/registro/",
            json={
                "username": username,
                "email": email,
                "password": password1,
                "rol": "cliente"  # Siempre cliente
            }
        )
        if response.status_code == 200:
            return redirect("login")
        else:
            return render(request, "registro.html", {"form": {"errors": True}})
    return render(request, "registro.html", {"form": {}})

def logout_view(request):
    request.session.flush()
    return redirect("index")

def admin_usuarios(request):
    if request.session.get("rol") != "administrador":
        return redirect("index")
    # Añadir usuario
    if request.method == "POST" and "add_user" in request.POST:
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        rol = request.POST["rol"]
        requests.post(
            "http://127.0.0.1:8001/registro/",
            json={
                "username": username,
                "email": email,
                "password": password,
                "rol": rol
            }
        )
        return redirect("admin-usuarios")
    # Editar usuario
    if request.method == "POST" and "edit_user" in request.POST:
        user_id = request.POST["user_id"]
        username = request.POST["edit_username"]
        email = request.POST["edit_email"]
        rol = request.POST["edit_rol"]
        requests.put(
            f"http://127.0.0.1:8001/usuarios/{user_id}",
            json={
                "username": username,
                "email": email,
                "rol": rol
            }
        )
        return redirect("admin-usuarios")
    # Borrar usuario
    if request.method == "POST" and "delete_user" in request.POST:
        user_id = request.POST["delete_user_id"]
        requests.delete(f"http://127.0.0.1:8001/usuarios/{user_id}")
        return redirect("admin-usuarios")
    # Mostrar usuarios
    response = requests.get("http://127.0.0.1:8001/usuarios/")
    usuarios = response.json() if response.status_code == 200 else []
    return render(request, "admin_usuarios.html", {"usuarios": usuarios})