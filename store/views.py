from django.shortcuts import render

def tienda(request):
    context = {}
    return render(request, 'store/tienda.html', context)

def carrito(request):
    context = {}
    return render(request, 'store/carrito.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)