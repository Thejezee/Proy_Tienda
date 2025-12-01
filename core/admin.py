from django.contrib import admin
from .models import Proveedor, Producto, Stock, MovimientoStock

admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(Stock)
admin.site.register(MovimientoStock)