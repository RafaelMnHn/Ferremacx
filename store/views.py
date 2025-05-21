from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Orden, DetalleOrden, Producto, DireccionEnvio
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
from django.utils import timezone
import requests
from django.urls import reverse
from django.conf import settings

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

# Crear transacción webpay
def iniciar_pago_rest(request):
    cliente = request.user
    orden = Orden.objects.filter(cliente=cliente, estado='pagada').last()

    if not orden:
        return redirect('tienda')

    url_retorno = request.build_absolute_uri(reverse('pago_exitoso_rest'))

    headers = {
        'Tbk-Api-Key-Id': settings.TBK_COMMERCE_CODE,
        'Tbk-Api-Key-Secret': settings.TBK_API_KEY_SECRET,
        'Content-Type': 'application/json'
    }

    data = {
        "buy_order": str(orden.id),
        "session_id": str(cliente.id),
        "amount": float(orden.total),
        "return_url": url_retorno
    }

    response = requests.post(
        'https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpayplus/v1/transactions',
        headers=headers,
        json=data
    )

    result = response.json()
    token = result['token']
    url = result['url']

    return redirect(f"{url}?token_ws={token}")

# Retorno / commit de transacción 
@csrf_exempt
def pago_exitoso_rest(request):
    token = request.GET.get('token_ws')
    if not token:
        return HttpResponse("Token no proporcionado", status=400)

    headers = {
        'Tbk-Api-Key-Id': settings.TBK_COMMERCE_CODE,
        'Tbk-Api-Key-Secret': settings.TBK_API_KEY_SECRET,
        'Content-Type': 'application/json'
    }

    response = requests.put(
        f'https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpayplus/v1/transactions/{token}',
        headers=headers
    )

    result = response.json()
    orden_id = result['buy_order']
    orden = Orden.objects.get(id=orden_id)
    orden.estado = 'completada'
    orden.save()

    return render(request, 'store/pago_exitoso.html', {'orden': orden})