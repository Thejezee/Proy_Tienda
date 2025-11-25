from django.shortcuts import render
from .models import Stock

def lista_productos(request):
    stocks = Stock.objects.select_related('producto', 'producto__categoria', 'producto__proveedor').all()
    return render(request, 'core/lista_productos.html', {'stocks': stocks})
