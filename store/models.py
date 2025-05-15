from django.contrib.auth.models import User
from django.db import models

# Usuario extendido/Pefil
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

# Producto y categoría
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    es_digital = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    @property
    def imageURL(self):
        try:
            url = self.imagen.url
        except:
            url = ''
        return url

# Orden y detalle de orden
class Orden(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('preparando', 'Preparando'),
        ('despachado', 'Despachado'),
        ('entregado', 'Entregado'),
    ]
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    retiro_en_tienda = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Orden #{self.id} - {self.cliente.username}"

class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"

# Dirección del envío 
class DireccionEnvio(models.Model):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    comuna = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.direccion

# Pago
class Pago(models.Model):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    metodo = models.CharField(max_length=50)  # transferencia, tarjeta, etc.
    confirmado = models.BooleanField(default=False)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    referencia_externa = models.CharField(max_length=100, blank=True, null=True)  # ID de la pasarela

    def __str__(self):
        return f"Pago de orden #{self.orden.id}"

# Bodega e inventario (API local)
class Bodega(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.producto} en {self.bodega}"
