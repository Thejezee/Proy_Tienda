from django.shortcuts import render
from .models import Producto, Stock

def lista_productos(request):
    # 1. Sacamos todos los productos de la BD
    productos = Producto.objects.all()
    
    # 2. Se los mandamos al HTML (que crearemos luego)
    return render(request, 'core/lista_productos.html', {
        'mis_productos': productos
    })