from django.urls import path
from . import views

urlpatterns = [
    #String vacio para url base 
    path('', views.tienda, name="tienda"),
    path('carrito/', views.carrito, name="carrito"),
    path('checkout/', views.checkout, name="checkout"),
    path('actualizar-item/', views.actualizarItem, name='actualizar-item'),
]