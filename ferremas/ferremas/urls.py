from django.contrib import admin
from django.urls import path
from pedidos import views as pedidos_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pedidos_views.index, name='index'),  # Página principal
    path('about/', pedidos_views.about, name='about'),  # Página "About"
    path('news/', pedidos_views.news, name='news'),  # Página "News"
    path('cart/', pedidos_views.cart, name='cart'),  # Página "Cart"
    path('checkout/', pedidos_views.checkout, name='checkout'),  # Página "Checkout"
    path('contact/', pedidos_views.contact, name='contact'),  # Página "Contact"
    path('shop/', pedidos_views.shop, name='shop'),  # Página "Shop"
    path('single-product/', pedidos_views.single_product, name='single-product'),  # Página "Single Product"
    path('single-news/', pedidos_views.single_news, name='single-news'),  # Página "Single News"
    path('index_2/', pedidos_views.index_2, name='index_2'),  # Página "Slider Home"
]