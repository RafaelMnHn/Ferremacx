from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.shortcuts import render, redirect
from .decorators import rol_requerido

# Login con redirección por grupo
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirigir según grupo
            if user.groups.filter(name='Administrador').exists():
                return redirect('admin_dashboard') 
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

#Registro con asignacion de grupo
def registro_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.warning(request, 'Las contraseñas no coinciden.')
            return redirect('registro')

        if User.objects.filter(username=username).exists():
            messages.warning(request, 'El nombre de usuario ya está en uso.')
            return redirect('registro')

        user = User.objects.create_user(username=username, email=email, password=password1)

        # Asignar al grupo "Cliente"
        grupo_cliente, creado = Group.objects.get_or_create(name='Cliente')
        user.groups.add(grupo_cliente)

        messages.success(request, 'Cuenta creada correctamente. Inicia sesión.')
        return redirect('login')

    return render(request, 'user/registro.html')


# Vistas protegidas
@rol_requerido('Vendedor')
def vista_vendedor(request):
    return render(request, 'user/vendedor_dashboard.html')

@rol_requerido('Bodeguero')
def vista_bodeguero(request):
    return render(request, 'user/bodeguero_dashboard.html')

@rol_requerido('Contador')
def vista_contador(request):
    return render(request, 'user/contador_dashboard.html')

@rol_requerido('Administrador')
def vista_administrador(request):
    return render(request, 'user/admin_dashboard.html')

#Recuperar contraseña
    # Diccionario temporal de tokens de prueba
    RECOVERY_TOKENS = {}

def recuperar_contraseña(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            token = get_random_string(length=6)
            RECOVERY_TOKENS[email] = token  # Simula guardar el token (DB futura)

            # Envío real por correo (API)
            # send_email(email, token)

            print(f"[SIMULADO] Código de recuperación para {email}: {token}")

        messages.info(request, 'Si el correo existe, se ha enviado un código de recuperación.')
        return redirect('recuperar')

    return render(request, 'user/recuperar.html')

#Restablecer contraseña
def restablecer_contraseña(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        token_ingresado = request.POST.get('token')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        user = User.objects.filter(email=email).first()
        token_correcto = RECOVERY_TOKENS.get(email)

        if not user:
            messages.warning(request, 'Usuario no encontrado.')
            return redirect('restablecer')

        if token_ingresado != token_correcto:
            messages.warning(request, 'Código incorrecto.')
            return redirect('restablecer')

        if password1 != password2:
            messages.warning(request, 'Las contraseñas no coinciden.')
            return redirect('restablecer')

        user.set_password(password1)
        user.save()

        # Opcional: eliminar token después de usarlo
        RECOVERY_TOKENS.pop(email, None)

        messages.success(request, 'Contraseña actualizada. Ahora puedes iniciar sesión.')
        return redirect('login')

    return render(request, 'user/restablecer.html')