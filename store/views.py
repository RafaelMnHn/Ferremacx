from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Orden, DetalleOrden, Producto
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def tienda(request):
    context_carrito = obtener_carrito(request)
    productos = Producto.objects.all()
    context = {
        'productos': productos,
        'cartItems': len(context_carrito['items']),
    }
    return render(request, 'store/tienda.html', context)

def carrito(request):
    datos = obtener_carrito(request)
    context = {
        'items': datos['items'],
        'orden': datos['orden'],
        'cartItems': datos['orden'].total_items,
    }
    return render(request, 'store/carrito.html', context)

def obtener_carrito(request):
    if request.user.is_authenticated:
        cliente = request.user
        orden = Orden.objects.filter(cliente=cliente, estado='pendiente').first()

        if not orden:
            orden = Orden.objects.create(cliente=cliente, estado='pendiente')

        items = orden.detalles.all()
    else:
        items = []
        orden = {'total': 0}

    return {'items': items, 'orden': orden}

@login_required(login_url='login')
def checkout(request):
    contexto_carrito = obtener_carrito(request)
    datos = obtener_carrito(request)
    context = {
        'items': contexto_carrito['items'],
        'orden': contexto_carrito['orden'],
        'cartItems': datos['orden'].total_items,
    }
    return render(request, 'store/checkout.html', context)

@csrf_exempt
@login_required(login_url='login')
def actualizarItem(request):
    data = json.loads(request.body)
    producto_id = data['productId']
    action = data['action']

    producto = Producto.objects.get(id=producto_id)
    orden = Orden.objects.filter(cliente=request.user, estado='pendiente').first()

    if not orden:
        orden = Orden.objects.create(cliente=request.user, estado='pendiente')

    item, created = DetalleOrden.objects.get_or_create(
        orden=orden,
        producto=producto,
        defaults={'precio_unitario': producto.precio, 'cantidad': 0}
    )

    if action == 'add':
        if item.cantidad < 10:
            item.cantidad += 1
    elif action == 'remove':
        item.cantidad -= 1

    if item.cantidad <= 0:
        item.delete()
    else:
        item.save()

    return JsonResponse('Ítem actualizado', safe=False)