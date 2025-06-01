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
    path('single-product/', ferremas_views.single_product, name='single-product'),  # Página "Single Product"
    path('login/', ferremas_views.login_view, name='login'),
    path('registro/', ferremas_views.registro_view, name='registro'),
    path('logout/', ferremas_views.logout_view, name='logout'),
    path('admin-usuarios/', ferremas_views.admin_usuarios, name='admin-usuarios'),
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('agregar-producto/', views.agregar_producto, name='agregar_producto'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)