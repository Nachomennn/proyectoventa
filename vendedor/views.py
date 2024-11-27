from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from productos.models import Producto, Categoria
from ventas.models import Venta
from jefeventa.models import EstadoDia
from ventas.models import VentaDetalle
from empleados.models import Empleado


def menu_vendedor(request):
    # Verifica si el día está iniciado
    estado_dia = EstadoDia.objects.filter(fecha=now().date()).first()
    dia_iniciado = estado_dia.estado if estado_dia else False

    # Obtener productos activos
    productos = Producto.objects.filter(estado=True)

    # Filtrar productos
    nombre_buscado = request.GET.get('nombre', '').strip()
    categoria_seleccionada = request.GET.get('categoria', '')

    if nombre_buscado:
        productos = productos.filter(nombre__icontains=nombre_buscado)
    if categoria_seleccionada:
        productos = productos.filter(categoria__id=categoria_seleccionada)

    categorias = Categoria.objects.all()

    # Redirigir al flujo de ventas si se selecciona un producto
    if request.method == 'POST':
        # Verifica si el usuario está autenticado
        if not request.user.is_authenticated:
            return redirect('/')  # Ajustado para redirigir a la página principal si no autenticado

        # Crear o recuperar la venta activa
        venta, created = Venta.objects.get_or_create(
            vendedor=request.user,  # Usa el usuario autenticado
            estado='abierta',  # Asegúrate de que la venta está abierta
            defaults={'total_neto': 0, 'total_con_iva': 0}
        )

        # Redirigir usando el ID de la venta
        return redirect('ventas:venta_en_curso', id=venta.id)

    return render(request, 'vendedor/menu_vendedor.html', {
        'dia_iniciado': dia_iniciado,
        'productos': productos,
        'categorias': categorias,
        'nombre_buscado': nombre_buscado,
        'categoria_seleccionada': categoria_seleccionada,
    })


# codigo para realizar venta de productos
from decimal import Decimal
def realizar_venta(request):
    # Filtros
    nombre_buscado = request.GET.get('nombre', '').strip()
    categoria_id = request.GET.get('categoria', '')

    # Obtener todos los productos activos
    productos = Producto.objects.filter(estado=1, stock__gt=0)

    # Aplicar filtros
    if nombre_buscado:
        productos = productos.filter(nombre__icontains=nombre_buscado)
    if categoria_id:
        productos = productos.filter(categoria__id=categoria_id)

    # Obtener todas las categorías para el filtro
    categorias = Categoria.objects.all()
    clientes = Cliente.objects.all()  # Para seleccionar cliente si es factura

    if request.method == 'POST':
        # Obtener datos del formulario
        tipo_documento = request.POST.get('tipo_documento', 'boleta')
        metodo_pago = request.POST.get('metodo_pago', 'efectivo')
        vendedor_run = request.POST.get('vendedor_run')
        cliente_rut = request.POST.get('cliente_rut')  # Cliente para factura
        productos_total = int(request.POST.get('productos-total', 0))

        # Validar vendedor
        try:
            empleado = Empleado.objects.get(run=vendedor_run)
        except Empleado.DoesNotExist:
            return render(request, 'vendedor/realizar_venta.html', {
                'productos': productos,
                'categorias': categorias,
                'clientes': clientes,
                'error': 'El vendedor con ese RUN no existe.',
            })

        # Validar cliente si es factura
        cliente = None
        if tipo_documento == 'factura':
            if not cliente_rut:
                return render(request, 'vendedor/realizar_venta.html', {
                    'productos': productos,
                    'categorias': categorias,
                    'clientes': clientes,
                    'error': 'Debe seleccionar un cliente para generar una factura.',
                })
            try:
                cliente = Cliente.objects.get(rut=cliente_rut)
            except Cliente.DoesNotExist:
                return render(request, 'vendedor/realizar_venta.html', {
                    'productos': productos,
                    'categorias': categorias,
                    'clientes': clientes,
                    'error': 'El cliente con ese RUT no existe.',
                })

        # Crear la venta
        venta = Venta.objects.create(
            vendedor=empleado,
            cliente=cliente,  # Guardar el cliente relacionado
            estado='cerrada',
            fecha=now(),
            total_neto=0,
            total_con_iva=0,
            tipo_documento=tipo_documento,
            metodo_pago=metodo_pago
        )

        total_neto = Decimal('0.00')
        productos_procesados = False  # Verifica si se procesaron productos correctamente

        # Procesar productos seleccionados
        for i in range(productos_total):
            codigo_barra = request.POST.get(f'productos-{i}-codigoBarra')
            cantidad = request.POST.get(f'productos-{i}-cantidad')

            if cantidad and codigo_barra:
                cantidad = int(cantidad)
                if cantidad > 0:
                    producto = get_object_or_404(Producto, codigoBarra=codigo_barra)

                    if cantidad <= producto.stock:
                        subtotal = producto.precio * cantidad
                        total_neto += subtotal
                        productos_procesados = True

                        # Crear detalle de venta
                        VentaDetalle.objects.create(
                            venta=venta,
                            producto=producto,
                            nombre=producto.nombre,
                            cantidad=cantidad,
                            precio_unitario=producto.precio,
                            subtotal=subtotal
                        )

                        # Actualizar stock
                        producto.stock -= cantidad
                        producto.save()

        if not productos_procesados:
            venta.delete()  # Borra la venta si no se procesaron productos
            return render(request, 'vendedor/realizar_venta.html', {
                'productos': productos,
                'categorias': categorias,
                'clientes': clientes,
                'error': 'No se seleccionaron productos válidos para la venta.',
            })

        # Calcular totales con o sin IVA
        if tipo_documento == 'factura':
            total_con_iva = total_neto * Decimal('1.19')
        else:
            total_con_iva = total_neto

        # Actualizar la venta
        venta.total_neto = total_neto
        venta.total_con_iva = total_con_iva
        venta.save()

        return redirect('ventas:venta_en_curso', id=venta.id)

    return render(request, 'vendedor/realizar_venta.html', {
        'productos': productos,
        'categorias': categorias,
        'clientes': clientes,
    })



def venta_en_curso(request, id):
    venta = get_object_or_404(Venta, id=id)
    detalles = VentaDetalle.objects.filter(venta=venta)

    return render(request, 'vendedor/venta_en_curso.html', {
        'venta': venta,
        'detalles': detalles
    })



def listar_ventas(request, origen=None):
    ventas = Venta.objects.all().order_by('-fecha')  # Lista todas las ventas ordenadas por fecha
    return render(request, 'ventas/listar_ventas.html', {
        'ventas': ventas,
        'origen': origen or 'vendedor',  # Por defecto, asume que es desde el menú del vendedor
    })




def detalles_venta(request, venta_id, origen=None):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = VentaDetalle.objects.filter(venta=venta)

    # Verificar si es factura y tiene cliente asociado
    cliente = venta.cliente if venta.tipo_documento == 'factura' and venta.cliente else None

    return render(request, 'ventas/detalles_venta.html', {
        'venta': venta,
        'detalles': detalles,
        'cliente': cliente,  # Incluye el cliente si es factura
        'origen': origen or 'vendedor',  # Por defecto, asume que es desde el menú del vendedor
    })



#-----------------------------------------------------------------

def anular_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    venta.estado = 'anulada'
    venta.save()
    return redirect('vendedor:listar_ventas', origen='vendedor')
#----------------------------------------------------------------



from cliente.models import Cliente

# Registrar Cliente
def registrar_cliente(request):
    if request.method == 'POST':
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        rut = request.POST.get('rut')
        direccion = request.POST.get('direccion')
        razon_social = request.POST.get('razon_social')
        giro = request.POST.get('giro')

        # Validar datos
        if not nombres or not apellidos or not rut:
            return render(request, 'cliente/registrar_cliente.html', {
                'error': 'Nombres, apellidos y RUT son campos requeridos.',
            })

        # Crear cliente
        Cliente.objects.create(
            rut=rut,
            nombres=nombres,
            apellidos=apellidos,
            direccion=direccion,
            razon_social=razon_social,
            giro=giro
        )
        return redirect('cliente:listar_cliente')  # Cambia según tu menú

    return render(request, 'cliente/registrar_cliente.html')



from django.shortcuts import render
from cliente.models import Cliente  # Importa el modelo Cliente correctamente

def listar_clientes(request):
    clientes = Cliente.objects.all()  # Obtén todos los clientes
    return render(request, 'cliente/listar_clientes.html', {'clientes': clientes})



# Editar Cliente
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        # Obtener datos del formulario
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        rut = request.POST.get('rut')
        direccion = request.POST.get('direccion')
        razon_social = request.POST.get('razon_social')
        giro = request.POST.get('giro')

        # Validar que los datos requeridos no estén vacíos
        if not nombres or not apellidos or not rut:
            return render(request, 'cliente/editar_cliente.html', {
                'cliente': cliente,
                'error': 'Nombres, apellidos y RUT son campos requeridos.',
            })

        # Actualizar el cliente
        cliente.nombres = nombres
        cliente.apellidos = apellidos
        cliente.rut = rut
        cliente.direccion = direccion
        cliente.razon_social = razon_social
        cliente.giro = giro
        cliente.save()

        # Redirigir a la lista de clientes
        return redirect('cliente:listar_cliente')

    return render(request, 'cliente/editar_cliente.html', {'cliente': cliente})


# Eliminar Cliente
def eliminar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id=id_cliente)
    cliente.delete()
    return redirect('cliente:listar_cliente')




from django.http import HttpResponse
from openpyxl import Workbook
from ventas.models import Venta

def exportar_ventas_excel(request):
    # Crear un archivo de Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Ventas"

    # Encabezados
    headers = ['ID', 'Fecha', 'Vendedor', 'Total Neto', 'Total con IVA', 'Tipo Documento']
    ws.append(headers)

    # Obtener las ventas de la base de datos
    ventas = Venta.objects.all()

    # Agregar las filas de datos
    for venta in ventas:
        # Asegúrate de eliminar la zona horaria de la fecha
        fecha_sin_tz = venta.fecha.replace(tzinfo=None) if venta.fecha else None
        ws.append([
            venta.id,
            fecha_sin_tz,  # Usar la fecha sin información de zona horaria
            f"{venta.vendedor.nombre} {venta.vendedor.apellido}" if venta.vendedor else "N/A",
            venta.total_neto,
            venta.total_con_iva,
            venta.tipo_documento,
        ])

    # Preparar la respuesta
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="ventas.xlsx"'
    wb.save(response)
    return response


from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.shortcuts import get_object_or_404
from ventas.models import Venta, VentaDetalle

def generar_pdf_venta(request, venta_id):
    # Obtener la venta y los detalles
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = VentaDetalle.objects.filter(venta=venta)

    # Crear respuesta HTTP con tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="venta_{venta.id}.pdf"'

    # Crear el documento PDF
    p = canvas.Canvas(response, pagesize=letter)
    ancho, alto = letter
    y = alto - 50

    # Encabezado
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, f"Detalles de la Venta - ID: {venta.id}")
    y -= 30
    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Fecha: {venta.fecha.strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 20
    p.drawString(50, y, f"Vendedor: {venta.vendedor.nombre} {venta.vendedor.apellido}")
    y -= 20
    p.drawString(50, y, f"Tipo Documento: {venta.tipo_documento}")
    y -= 20
    p.drawString(50, y, f"Total Neto: ${venta.total_neto}")
    y -= 20
    p.drawString(50, y, f"Total con IVA: ${venta.total_con_iva}")
    y -= 40

    # Datos del Cliente (si aplica)
    if venta.cliente:
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Datos del Cliente")
        y -= 20
        p.setFont("Helvetica", 12)
        p.drawString(50, y, f"RUT: {venta.cliente.rut}")
        y -= 20
        p.drawString(50, y, f"Nombres: {venta.cliente.nombres} {venta.cliente.apellidos}")
        y -= 20
        p.drawString(50, y, f"Dirección: {venta.cliente.direccion}")
        y -= 40

    # Detalles de los productos vendidos
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Productos Vendidos")
    y -= 20
    p.setFont("Helvetica", 12)
    for detalle in detalles:
        p.drawString(50, y, f"Producto: {detalle.nombre}")
        y -= 20
        p.drawString(70, y, f"Cantidad: {detalle.cantidad}, Precio Unitario: ${detalle.precio_unitario}, Subtotal: ${detalle.subtotal}")
        y -= 30
        if y < 100:  # Salto de página si no hay espacio
            p.showPage()
            y = alto - 50

    p.showPage()
    p.save()

    return response
