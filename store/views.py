from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Orden, DetalleOrden, Producto
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.utils import timezone

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
    datos = obtener_carrito(request)
    orden = datos['orden']

    if not datos['items']:
        return redirect('tienda')

    context = {
        'items': datos['items'],
        'orden': datos['orden'],
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

@csrf_exempt
@login_required(login_url='login')
def procesarOrden(request):
    data = json.loads(request.body)
    cliente = request.user
    total_frontend = float(data['total']) 
    orden = Orden.objects.filter(cliente=cliente, estado='pendiente').first()

    # Buscar orden pendiente
    if not orden:
        return JsonResponse({'error': 'Orden no encontrada'}, status=404)

    # Comparar montos
    if total_frontend != float(orden.total):
        return JsonResponse({'error': 'Monto inconsistente'}, status=400)

    # Crear dirección si no existe
    DireccionEnvio.objects.get_or_create(
        orden=orden,
        defaults={
            'cliente': cliente,
            'direccion': data['direccion'],
            'ciudad': data['ciudad'],
            'region': data['region'],
            'comuna': data['comuna']
        }
    ) 

    # Estado de orden
    orden.estado = 'confirmada'
    orden.fecha_confirmacion = timezone.now()
    orden.save()

    return JsonResponse('Pedido procesado correctamente', safe=False)