from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    # Puedes añadir más vistas por rol aquí
]