from django.contrib import admin
from .models import Producto, Categoria, Orden, DetalleOrden, DireccionEnvio, Pago, Bodega, Inventario

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Orden)
admin.site.register(DetalleOrden)
admin.site.register(DireccionEnvio)
admin.site.register(Pago)
admin.site.register(Bodega)
admin.site.register(Inventario)
