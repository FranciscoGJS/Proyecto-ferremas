from django.shortcuts import render

# Vista para la página principal
def index(request):
    return render(request, 'index.html')

def index_2(request):
    return render(request, 'index_2.html')

# Vista para la página "About"
def about(request):
    return render(request, 'about.html')

# Vista para la página "News"
def news(request):
    return render(request, 'news.html')

# Vista para la página "Cart"
def cart(request):
    return render(request, 'cart.html')

# Vista para la página "Checkout"
def checkout(request):
    return render(request, 'checkout.html')

# Vista para la página "Contact"
def contact(request):
    return render(request, 'contact.html')

def shop(request):
    return render(request, 'shop.html')

def single_product(request):
    return render(request, 'single-product.html')

def single_news(request):
    return render(request, 'single-news.html')