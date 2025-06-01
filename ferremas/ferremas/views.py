from django.shortcuts import render, redirect
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os



def add_to_cart(request):
    if request.method == "POST":
        producto_id = request.POST.get("producto_id")
        cantidad = int(request.POST.get("cantidad", 1))
        response = requests.get("http://localhost:3002/productos")
        productos = response.json() if response.status_code == 200 else []
        producto = next((p for p in productos if str(p[0]) == str(producto_id)), None)
        if not producto:
            return JsonResponse({"success": False, "error": "Producto no encontrado"})
        cart = request.session.get("cart", {})
        if producto_id in cart:
            cart[producto_id]["cantidad"] += cantidad
        else:
            cart[producto_id] = {
                "id": producto[0],
                "nombre": producto[1],
                "descripcion": producto[2],
                "precio": producto[3],
                "stock": producto[4],
                "categoria": producto[5],
                "marca": producto[6],
                "imagen": producto[7] if len(producto) > 7 else "",  # <-- AGREGA ESTA LÍNEA
                "cantidad": cantidad,
            }
        request.session["cart"] = cart
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Método no permitido"})

def index(request):
    return render(request, 'index.html')


# Vista para la página "About"
def about(request):
    return render(request, 'about.html')


# Vista para la página "Cart"
def cart(request):
    cart = request.session.get("cart", {})
    subtotal = sum(float(item["precio"]) * int(item["cantidad"]) for item in cart.values())
    return render(request, "cart.html", {"subtotal": subtotal})

# Vista para la página "Contact"
def contact(request):
    return render(request, 'contact.html')

# ...existing code...

def shop(request):
    try:
        response = requests.get("http://localhost:3002/productos")
        productos = response.json() if response.status_code == 200 else []
    except Exception:
        productos = []
    return render(request, 'shop.html', {"productos": productos})

# ...existing code...

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
                "rol": "cliente"  
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

@csrf_exempt
def update_cart(request):
    if request.method == "POST":
        producto_id = request.POST.get("producto_id")
        cantidad = int(request.POST.get("cantidad", 1))
        cart = request.session.get("cart", {})
        if producto_id in cart:
            cart[producto_id]["cantidad"] = cantidad
            request.session["cart"] = cart
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "Producto no encontrado"})
    return JsonResponse({"success": False, "error": "Método no permitido"})

@csrf_exempt
def remove_from_cart(request):
    if request.method == "POST":
        producto_id = request.POST.get("producto_id")
        cart = request.session.get("cart", {})
        if producto_id in cart:
            del cart[producto_id]
            request.session["cart"] = cart
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "Producto no encontrado"})
    return JsonResponse({"success": False, "error": "Método no permitido"})


def agregar_producto(request):
    if request.session.get("rol") != "administrador":
        return redirect("index")

    producto_editar = None

    # Obtener productos existentes
    response = requests.get("http://localhost:3002/productos")
    productos_raw = response.json() if response.status_code == 200 else []
    productos = [
        {
            "id": p[0],
            "nombre": p[1],
            "descripcion": p[2],
            "precio": p[3],
            "stock": p[4],
            "categoria": p[5],
            "marca": p[6],
            "imagen": p[7] if len(p) > 7 else "",
        }
        for p in productos_raw
    ]

    if request.method == "POST":
        # EDITAR: cargar datos en el formulario
        if "edit_id" in request.POST:
            edit_id = request.POST["edit_id"]
            producto_editar = next((p for p in productos if str(p["id"]) == str(edit_id)), None)

        # ELIMINAR
        elif "delete_id" in request.POST:
            delete_id = request.POST["delete_id"]
            requests.delete(f"http://localhost:3002/productos/{delete_id}")
            return redirect("agregar_producto")

        # AGREGAR o ACTUALIZAR
        elif "nombre" in request.POST:
            nombre = request.POST["nombre"]
            descripcion = request.POST["descripcion"]
            precio = request.POST["precio"]
            stock = request.POST["stock"]
            categoria = request.POST["categoria"]
            marca = request.POST["marca"]
            imagen = request.FILES.get("imagen")
            imagen_url = ""
            if imagen:
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "productos"))
                filename = fs.save(imagen.name, imagen)
                imagen_url = fs.url("productos/" + filename)
            else:
                # Si es edición y no se sube nueva imagen, mantener la anterior
                imagen_url = request.POST.get("imagen_actual", "")

            data = {
                "nombre": nombre,
                "descripcion": descripcion,
                "precio": precio,
                "stock": stock,
                "categoria": categoria,
                "marca": marca,
                "imagen": imagen_url,
            }
            producto_id = request.POST.get("producto_id")
            if producto_id:  # Actualizar
                requests.put(f"http://localhost:3002/productos/{producto_id}", json=data)
            else:  # Agregar
                requests.post("http://localhost:3002/productos", json=data)
            return redirect("agregar_producto")

        # Recargar productos si solo fue editar (mostrar en formulario)
        response = requests.get("http://localhost:3002/productos")
        productos_raw = response.json() if response.status_code == 200 else []
        productos = [
            {
                "id": p[0],
                "nombre": p[1],
                "descripcion": p[2],
                "precio": p[3],
                "stock": p[4],
                "categoria": p[5],
                "marca": p[6],
                "imagen": p[7] if len(p) > 7 else "",
            }
            for p in productos_raw
        ]

    return render(request, "agregar_producto.html", {
        "productos": productos,
        "producto_editar": producto_editar,
    })