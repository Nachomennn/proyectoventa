from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import CategoriaForm


def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/listar_productos.html', {'productos': productos})


from django.shortcuts import render, redirect
from .models import Producto, Categoria
from django.contrib import messages

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
        return redirect('productos:listar_productos')

    categorias = Categoria.objects.all()
    return render(request, 'productos/agregar_producto.html', {'categorias': categorias})


import os
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria
from django.contrib import messages

def editar_producto(request, codigo):
    producto = Producto.objects.get(codigoBarra=codigo)
    if request.method == 'POST':
        # Actualizar los campos
        producto.nombre = request.POST['nombre']
        producto.precio = request.POST['precio']
        producto.stock = request.POST['stock']
        producto.descripcion = request.POST['descripcion']
        categoria_id = request.POST['categoria']
        producto.categoria = Categoria.objects.get(id=categoria_id)

        # Verificar si hay una nueva foto
        nueva_foto = request.FILES.get('foto')
        if nueva_foto:
            # Si existe una foto anterior, eliminarla del sistema de archivos
            if producto.foto and producto.foto.path:  # Asegurarse de que exista `foto.path`
                if os.path.isfile(producto.foto.path):
                    os.remove(producto.foto.path)
            # Asignar la nueva foto
            producto.foto = nueva_foto

        # Guardar los cambios en el producto
        producto.save()
        messages.success(request, "Producto editado con éxito.")
        return redirect('productos:listar_productos')

    categorias = Categoria.objects.all()
    return render(request, 'productos/editar_producto.html', {'producto': producto, 'categorias': categorias})

def eliminar_producto(request, codigo):
    producto = get_object_or_404(Producto, codigoBarra=codigo)
    producto.delete()
    messages.success(request, "Producto eliminado con éxito.")
    return redirect('productos:listar_productos')



def registrar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda la categoría en la base de datos
            return redirect('productos:listar_categoria')  # Cambia esto según la URL para listar las categorías
    else:
        form = CategoriaForm()
    return render(request, 'productos/registrar_categoria.html', {'form': form})


def listar_categoria(request):
    categorias = Categoria.objects.all()  # Obtén todas las categorías de la base de datos
    return render(request, 'productos/listar_categoria.html', {'categorias': categorias})


def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()  # Guarda la categoría en la base de datos
            return redirect('productos:listar_categoria')  # Cambia esto según la URL para listar las categorías
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'productos/editar_categoria.html', {'form': form})

def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    return redirect('productos:listar_categoria')  # Cambia esto según la URL para listar las categorías