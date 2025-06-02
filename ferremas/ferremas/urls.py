from django.contrib import admin
from django.urls import path
from ferremas import views as ferremas_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ferremas_views.index, name='index'),  # Página principal
    path('about/', ferremas_views.about, name='about'),  # Página "About"
    path('cart/', ferremas_views.cart, name='cart'),  # Página "Cart"
    path('contact/', ferremas_views.contact, name='contact'),  # Página "Contact"
    path('shop/', ferremas_views.shop, name='shop'),  # Página "Shop"
    path('producto/<int:producto_id>/', views.single_product, name='single-product'),
    path('login/', ferremas_views.login_view, name='login'),
    path('registro/', ferremas_views.registro_view, name='registro'),
    path('logout/', ferremas_views.logout_view, name='logout'),
    path('admin-usuarios/', ferremas_views.admin_usuarios, name='admin-usuarios'),
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('agregar-producto/', views.agregar_producto, name='agregar_producto'),
    path('transferencia/', views.transferencia_view, name='transferencia'),
    path('pagos-transferencia/', views.pagos_transferencia_contador, name='pagos_transferencia'),
    path('registrar-pago-paypal/', views.registrar_pago_paypal, name='registrar_pago_paypal'),
    path('pedidos-bodeguero/', views.pedidos_bodeguero, name='pedidos_bodeguero'),
    path('gracias-transferencia/', ferremas_views.gracias_transferencia, name='gracias_transferencia'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('pedidos-vendedor/', views.pedidos_vendedor, name='pedidos_vendedor'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)