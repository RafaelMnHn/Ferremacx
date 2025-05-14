from django.shortcuts import render
from .models import Producto

def tienda(request):
    productos = Producto.objects.all()
    context = {'productos': productos}
    return render(request, 'store/tienda.html', context)

def carrito(request):
    context = {}
    return render(request, 'store/carrito.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)