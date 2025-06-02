from django.shortcuts import render, redirect
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from .models import PagoTransferencia
import json


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
        stock_disponible = int(producto[4])
        cantidad_actual = cart.get(producto_id, {}).get("cantidad", 0)
        if cantidad_actual + cantidad > stock_disponible:
            return JsonResponse({"success": False, "error": "No hay suficiente stock disponible"})
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
                "imagen": producto[7] if len(producto) > 7 else "",
                "cantidad": cantidad,
            }
        request.session["cart"] = cart
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Método no permitido"})

def index(request):
    # Obtener productos desde la API
    response = requests.get("http://localhost:3002/productos")
    productos = response.json() if response.status_code == 200 else []
    productos_destacados = productos[:3]  # Solo los 3 primeros
    return render(request, "index.html", {
        "productos_destacados": productos_destacados,
    })


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



def shop(request):
    # Obtener productos desde tu API
    response = requests.get("http://localhost:3002/productos")
    productos = response.json() if response.status_code == 200 else []

    # Obtener valor del dólar
    dolar = None
    try:
        dolar_resp = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        if dolar_resp.status_code == 200:
            data = dolar_resp.json()
            # Cambia 'CLP' por la moneda local que desees mostrar
            dolar = data["rates"].get("CLP")
    except Exception:
        dolar = None

    return render(request, "shop.html", {
        "productos": productos,
        "dolar": dolar,
    })


def single_product(request, producto_id):
    response = requests.get("http://localhost:3002/productos")
    productos = response.json() if response.status_code == 200 else []
    producto = next((p for p in productos if int(p[0]) == int(producto_id)), None)
    if not producto:
        return render(request, "404.html", status=404)
    return render(request, 'single-product.html', {'producto': producto})

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
@csrf_exempt
def update_cart(request):
    if request.method == "POST":
        producto_id = request.POST.get("producto_id")
        cantidad = int(request.POST.get("cantidad", 1))
        cart = request.session.get("cart", {})
        if producto_id in cart:
            stock_disponible = int(cart[producto_id]["stock"])
            if cantidad > stock_disponible:
                return JsonResponse({"success": False, "error": "No hay suficiente stock disponible"})
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

def transferencia_view(request):
    cart = request.session.get("cart", {})
    subtotal = sum(float(item["precio"]) * int(item["cantidad"]) for item in cart.values())
    if request.method == "POST":
        usuario = request.session.get("username")
        monto = request.POST["monto"]
        detalles = request.POST.get("detalles", "")
        PagoTransferencia.objects.create(
            usuario=usuario,
            monto=monto,
            detalles=detalles,
            tipo_pago="transferencia"
        )
        request.session["cart"] = {}
        return redirect("gracias_transferencia")
    return render(request, "transferencia.html", {
        "cart": cart,
        "subtotal": subtotal
    })

def pagos_transferencia_contador(request):
    rol = request.session.get("rol")
    if rol not in ["contador", "administrador"]:
        return redirect("index")
    if request.method == "POST":
        accion = request.POST.get("accion")
        if accion == "eliminar_todos":
            # Solo ocultar de la vista del contador, no borrar de la base de datos
            PagoTransferencia.objects.filter(tipo_pago="transferencia").update(estado="oculto_contador")
        else:
            pago_id = request.POST.get("pago_id")
            pago = PagoTransferencia.objects.get(id=pago_id)
            if accion == "aceptar":
                pago.estado = "aceptado"
            elif accion == "rechazar":
                pago.estado = "rechazado"
            pago.save()
    # Solo mostrar los que no están ocultos para el contador
    pagos = PagoTransferencia.objects.filter(tipo_pago="transferencia").exclude(estado="oculto_contador").order_by('-fecha')
    return render(request, "pagos_transferencia.html", {"pagos": pagos})

def registrar_pago_paypal(request):
    if request.method == "POST":
        data = json.loads(request.body)
        usuario = data.get("usuario")
        monto = data.get("monto")
        detalles = data.get("detalles", "")
        PagoTransferencia.objects.create(
            usuario=usuario,
            monto=monto,
            estado="aceptado",
            detalles=detalles,
            tipo_pago="tarjeta"
        )
        request.session["cart"] = {}
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

def pedidos_bodeguero(request):
    rol = request.session.get("rol")
    if rol not in ["bodeguero", "administrador"]:
        return redirect("index")
    pedidos = PagoTransferencia.objects.filter(
        estado__in=["pendiente", "aceptado"]
    ).order_by('-fecha')
    if request.method == "POST":
        pedido_id = request.POST.get("pedido_id")
        accion = request.POST.get("accion")
        pedido = PagoTransferencia.objects.get(id=pedido_id)
        if accion == "listo":
            pedido.estado = "listo"
            pedido.save()
        elif accion == "eliminar_bodeguero":
            pedido.estado = "oculto_bodeguero"
            pedido.save()
        return redirect("pedidos_bodeguero")
    return render(request, "PedidoPagoTarjeta.html", {"pedidos": pedidos})

def gracias_transferencia(request):
    return render(request, "gracias_transferencia.html")

def mis_pedidos(request):
    usuario = request.session.get("username")
    rol = request.session.get("rol")
    if not usuario:
        return redirect("login")
    if rol == "administrador":
        pedidos = PagoTransferencia.objects.all().order_by('-fecha')
    else:
        pedidos = PagoTransferencia.objects.filter(usuario=usuario, estado="entregado").order_by('-fecha')
    return render(request, "mis_pedidos.html", {"pedidos": pedidos, "rol": rol})

def pedidos_vendedor(request):
    rol = request.session.get("rol")
    if rol not in ["vendedor", "administrador"]:
        return redirect("index")
    pedidos = PagoTransferencia.objects.filter(estado="listo").order_by('-fecha')
    if request.method == "POST":
        pedido_id = request.POST.get("pedido_id")
        pedido = PagoTransferencia.objects.get(id=pedido_id)
        pedido.estado = "entregado"
        pedido.save()
        return redirect("pedidos_vendedor")
    return render(request, "pedidos_vendedor.html", {"pedidos": pedidos})