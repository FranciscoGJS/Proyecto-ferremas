from django.shortcuts import render

# Vista para la página principal
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