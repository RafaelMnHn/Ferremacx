from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('recuperar/', views.recuperar_contraseña, name='recuperar'),
    path('restablecer/', views.restablecer_contraseña, name='restablecer'),
    # Puedes añadir más vistas por rol aquí
]