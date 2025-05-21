from django.urls import path
from . import views

urlpatterns = [
    path('', views.tienda, name="tienda"),
    path('carrito/', views.carrito, name="carrito"),
    path('checkout/', views.checkout, name="checkout"),
    path('actualizar-item/', views.actualizarItem, name='actualizar-item'),
    path('procesar-orden/', views.procesarOrden, name='procesar-orden'),

    path('iniciar-pago-rest/', views.iniciar_pago_rest, name='iniciar-pago-rest'),
    path('pago-exitoso-rest/', views.pago_exitoso_rest, name='pago_exitoso_rest'),

]