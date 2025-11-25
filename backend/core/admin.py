from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db.models import Sum
from .models import Categoria, Proveedor, Producto, Stock, MovimientoStock

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['sku', 'nombre', 'categoria', 'proveedor', 'precio_venta', 'stock_total']
    list_filter = ['categoria', 'proveedor']
    search_fields = ['sku', 'nombre']
    def stock_total(self, obj):
        total = Stock.objects.filter(producto=obj).aggregate(t=Sum('cantidad'))['t'] or 0
        return total
    stock_total.short_description = "Stock Total"

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['producto', 'ubicacion', 'cantidad', 'alerta']
    list_editable = ['cantidad']
    list_filter = ['ubicacion']
    def alerta(self, obj):
        if obj.bajo_stock():
            return mark_safe('<b style="color:red;">BAJO STOCK</b>')
        return "Normal"
    alerta.short_description = "Estado"

@admin.register(MovimientoStock)
class MovimientoStockAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'producto', 'tipo', 'cantidad', 'usuario']
    list_filter = ['tipo', 'fecha']
    date_hierarchy = 'fecha'
