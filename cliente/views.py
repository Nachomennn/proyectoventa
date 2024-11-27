from django.shortcuts import render
from .models import Cliente

def listar_cliente(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/lista_clientes.html', {'clientes': clientes})