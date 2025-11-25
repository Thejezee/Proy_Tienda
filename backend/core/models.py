from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self): return self.nombre
    class Meta: verbose_name_plural = "Categorías"

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True, null=True)
    def __str__(self): return self.nombre

class Producto(models.Model):
    sku = models.CharField("Código", max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    stock_minimo = models.IntegerField(default=10)
    def __str__(self): return f"{self.sku} - {self.nombre}"

class Stock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ubicacion = models.CharField(max_length=50)
    cantidad = models.IntegerField(default=0)
    def bajo_stock(self):
        return self.cantidad <= self.producto.stock_minimo
    def __str__(self):
        return f"{self.producto} → {self.ubicacion}: {self.cantidad}"

class MovimientoStock(models.Model):
    TIPO = [('COMPRA','Compra'),('VENTA','Venta'),('DEVOLUCION','Devolución'),('AJUSTE+','Ajuste +'),('AJUSTE-','Ajuste -')]
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    motivo = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return f"{self.fecha.strftime('%d/%m %H:%M')} | {self.tipo} | {self.cantidad}"
