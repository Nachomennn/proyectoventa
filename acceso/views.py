from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from empleados.models import Empleado

def iniciar_sesion(request):
    if request.method == 'POST':
        run = request.POST['run'].strip()
        contrasena = request.POST['contrasena']

        # Busca el empleado por su run
        empleado = Empleado.objects.filter(run=run).first()

        if empleado:
            # Verifica la contraseña
            if check_password(contrasena, empleado.contrasena):
                # Redirige según el rol del empleado
                if empleado.rol == 'jefe':
                    return redirect('jefeventa:menu_jefe')
                elif empleado.rol == 'vendedor':
                    return redirect('vendedor:menu_vendedor')
                else:
                    messages.error(request, "Rol no autorizado.")
            else:
                messages.error(request, "Contraseña incorrecta.")
        else:
            messages.error(request, "RUN no encontrado.")
    
    return render(request, 'acceso/iniciar_sesion.html')





def menu_jefe(request):
    return render(request, 'jefeventa/menu_jefe.html')

def menu_vendedor(request):
    return render(request, 'vendedor/menu_vendedor.html')

def cerrar_sesion(request):
    return redirect('acceso:iniciar_sesion')
