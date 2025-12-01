from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.contrib import messages # <--- 1. IMPORTANTE: Librería de mensajes
from .models import Producto, Stock, MovimientoStock
from .forms import MovimientoForm, ProductoForm



def pagina_inicio(request):
    return render(request, 'core/inicio.html')


@login_required
def lista_productos(request):
    busqueda = request.GET.get('q')
    if busqueda:
        productos = Producto.objects.filter(
            Q(nombre__icontains=busqueda) | 
            Q(proveedor__nombre__icontains=busqueda)
        )
    else:
        productos = Producto.objects.all()

    # KPIs
    total_productos = productos.count()
    productos_bajo_stock = 0
    valor_inventario = 0

    for p in productos:
        stock_fisico = Stock.objects.filter(producto=p).first()
        p.total_stock = stock_fisico.cantidad if stock_fisico else 0
        valor_inventario += p.total_stock * p.precio
        if p.total_stock < p.min_stock:
            productos_bajo_stock += 1

    # Gráfico
    datos_grafico = Producto.objects.values('proveedor__nombre').annotate(total=Count('id'))
    labels_grafico = [item['proveedor__nombre'] if item['proveedor__nombre'] else 'Sin Proveedor' for item in datos_grafico]
    data_grafico = [item['total'] for item in datos_grafico]

    return render(request, 'core/lista_productos.html', {
        'mis_productos': productos,
        'total_productos': total_productos,
        'productos_bajo_stock': productos_bajo_stock,
        'valor_inventario': valor_inventario,
        'labels_grafico': labels_grafico,
        'data_grafico': data_grafico,
    })

# --- VISTA 2: REGISTRAR MOVIMIENTO ---
@login_required
def registrar_movimiento(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save()
            
            # Actualizar Stock
            stock_fisico, created = Stock.objects.get_or_create(
                producto=movimiento.producto,
                defaults={'ubicacion': 'Tienda Principal', 'cantidad': 0}
            )
            
            if movimiento.tipo == 'ENTRADA':
                stock_fisico.cantidad += movimiento.cantidad
                # 2. MENSAJE DE ÉXITO
                messages.success(request, f'✅ Entrada de {movimiento.cantidad} u. registrada para {movimiento.producto}')
            else:
                stock_fisico.cantidad -= movimiento.cantidad
                messages.success(request, f'📉 Salida de {movimiento.cantidad} u. registrada para {movimiento.producto}')
            
            stock_fisico.save()
            return redirect('inicio')
    else:
        form = MovimientoForm()

    return render(request, 'core/form_movimiento.html', {'form': form})

# --- VISTA 3: HISTORIAL ---
@login_required
def historial_movimientos(request):
    movimientos = MovimientoStock.objects.all().order_by('-fecha')
    return render(request, 'core/historial.html', {'movimientos': movimientos})

# --- VISTA 4: EDITAR PRODUCTO ---
@login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            # MENSAJE DE ÉXITO
            messages.success(request, f'✏️ Producto "{producto.nombre}" actualizado correctamente.')
            return redirect('inicio')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'core/form_producto.html', {'form': form})

# --- VISTA 5: ELIMINAR PRODUCTO ---
@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        nombre_prod = producto.nombre
        producto.delete()
        # MENSAJE DE ÉXITO (Advertencia)
        messages.warning(request, f'🗑️ El producto "{nombre_prod}" ha sido eliminado.')
        return redirect('inicio')
    return render(request, 'core/confirmar_eliminar.html', {'producto': producto})