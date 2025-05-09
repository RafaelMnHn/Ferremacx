from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirigir según grupo
            if user.groups.filter(name='Administrador').exists():
                return redirect('admin_dashboard')  # Ruta a definir
            elif user.groups.filter(name='Vendedor').exists():
                return redirect('vista_vendedor')
            elif user.groups.filter(name='Bodeguero').exists():
                return redirect('vista_bodeguero')
            elif user.groups.filter(name='Contador').exists():
                return redirect('vista_contador')
            elif user.groups.filter(name='Cliente').exists():
                return redirect('tienda')  # Vista tienda
            else:
                messages.warning(request, 'Tu cuenta no tiene un rol asignado.')
                return redirect('login')
        else:
            messages.warning(request, 'Credenciales inválidas')
            return redirect('login')

    return render(request, 'user/login.html')