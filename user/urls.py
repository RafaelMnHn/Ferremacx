from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('recuperar/', views.recuperar_contraseña, name='recuperar'),
    path('restablecer/', views.restablecer_contraseña, name='restablecer'),

    # Vistas protegidas
    path('vendedor/', views.vista_vendedor, name='vista_vendedor'),
    path('bodeguero/', views.vista_bodeguero, name='vista_bodeguero'),
    path('contador/', views.vista_contador, name='vista_contador'),
    path('admin/', views.vista_administrador, name='admin_dashboard'),
]