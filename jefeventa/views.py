from django.shortcuts import render, redirect, get_object_or_404
from empleados.models import Empleado
from productos.models import Categoria, Producto
from django.contrib import messages
from django.utils.timezone import now
from jefeventa.models import EstadoDia



# menu de jefe de ventas

def menu_jefe(request):
    # Obtener todos los productos activos (sin filtros)
    productos = Producto.objects.filter(estado=True)
    return render(request, 'jefeventa/menu_jefe.html', {
        'productos': productos,
    })






def registrar_empleado(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        run = request.POST.get('run')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        direccion = request.POST.get('direccion')
        rol = request.POST.get('rol')
        contrasena = request.POST.get('contrasena')

        # Validaciones y guardado
        if Empleado.objects.filter(run=run).exists():
            messages.error(request, "El RUN ya está registrado.")
        else:
            Empleado.objects.create(
                usuario=usuario,
                run=run,
                nombre=nombre,
                apellido=apellido,
                direccion=direccion,
                rol=rol,
                contrasena=contrasena  # Asegúrate de encriptarla si es necesario
            )
            messages.success(request, "Empleado registrado con éxito.")
            return redirect('jefeventa:menu_jefe')  # Redirigir a la lista de empleados

    return render(request, 'jefeventa/menu_jefe.html')



# Iniciar el día
def iniciar_dia(request):
    # Verifica si ya existe un estado para el día actual
    estado_dia, creado = EstadoDia.objects.get_or_create(fecha=now().date())
    if not estado_dia.estado:
        estado_dia.estado = True  # Marca el día como iniciado
        estado_dia.save()
        messages.success(request, "El día ha sido iniciado correctamente.")
    else:
        messages.warning(request, "El día ya estaba iniciado.")
    return redirect('jefeventa:menu_jefe')


# Cerrar el día
def cerrar_dia(request):
    # Verifica si ya existe un estado para el día actual
    estado_dia = EstadoDia.objects.filter(fecha=now().date()).first()
    if estado_dia and estado_dia.estado:
        estado_dia.estado = False  # Marca el día como cerrado
        estado_dia.save()
        messages.success(request, "El día ha sido cerrado correctamente.")
    else:
        messages.warning(request, "El día ya estaba cerrado o no estaba iniciado.")
    return redirect('jefeventa:menu_jefe')



# Listar empleados
def listar_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'jefeventa/listar_empleados.html', {'empleados': empleados})


# Editar empleado
def editar_empleado(request, run):
    empleado = get_object_or_404(Empleado, run=run)
    if request.method == 'POST':
        # Actualiza todos los campos del empleado
        empleado.usuario = request.POST.get('usuario')
        empleado.nombre = request.POST.get('nombre')
        empleado.apellido = request.POST.get('apellido')
        empleado.direccion = request.POST.get('direccion')
        empleado.rol = request.POST.get('rol')
        empleado.save()
        # Redirige a la lista de empleados usando el espacio de nombres
        return redirect('jefeventa:listar_empleados')
    return render(request, 'jefeventa/editar_empleado.html', {'empleado': empleado})

# Eliminar empleado
def eliminar_empleado(request, run):
    empleado = get_object_or_404(Empleado, run=run)
    empleado.delete()
    # Redirige a la lista de empleados inmediatamente después de eliminar
    return redirect('jefeventa:listar_empleados')


# gestiones de productos

def agregar_producto(request):
    if request.method == 'POST':
        codigoBarra = request.POST['codigoBarra']
        nombre = request.POST['nombre']
        precio = request.POST['precio']
        stock = request.POST['stock']
        descripcion = request.POST['descripcion']
        categoria_id = request.POST['categoria']
        categoria = Categoria.objects.get(id=categoria_id)
        foto = request.FILES.get('foto')

        Producto.objects.create(
            codigoBarra=codigoBarra,
            nombre=nombre,
            precio=precio,
            stock=stock,
            descripcion=descripcion,
            categoria=categoria,
            foto=foto,
        )
        messages.success(request, "Producto agregado con éxito.")
        return redirect('jefeventa:menu_jefe')

    categorias = Categoria.objects.all()
    return render(request, 'productos/agregar_producto.html', {'categorias': categorias})  # Nueva vista para agregar producto

def listar_productos(request):
    return render(request, 'productos/listar_productos.html')  # Nueva vista para listar productos

def eliminar_producto(request, codigo):
    return render(request, 'productos/eliminar_producto.html')  # Nueva vista para eliminar producto

def editar_producto(request, codigo):
    return render(request, 'productos/editar_producto.html')  # Nueva vista para editar producto

def ver_venta(request, id_venta):
    return render(request, 'ventas/ver_venta.html')  # Nueva vista para ver venta

def menu_jefe(request):
    categorias = Categoria.objects.all()  # Asumiendo que Categoria es tu modelo
    return render(request, 'jefeventa/menu_jefe.html', {'categorias': categorias})
    