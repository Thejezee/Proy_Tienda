from django.db import models
from django.contrib.auth.models import User

# 1. PROVEEDOR (Tabla 1 de la imagen)
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Proveedores"

# 2. PRODUCTO (Tabla 2 de la imagen)
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True, verbose_name="Código SKU")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    # "Alertas por bajo inventario" (Requisito de la imagen)
    min_stock = models.IntegerField(default=5, verbose_name="Stock Mínimo (Alerta)")
    
    # "Búsqueda por proveedor" (Requisito de la imagen)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)
    
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

# 3. STOCK (Tabla 3 de la imagen - "por ubicación")
class Stock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="stocks")
    ubicacion = models.CharField(max_length=50, verbose_name="Ubicación en Tienda")
    cantidad = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.producto.nombre} en {self.ubicacion}: {self.cantidad}"

# 4. MOVIMIENTO STOCK (Tabla 4 de la imagen)
class MovimientoStock(models.Model):
    TIPOS = [
        ('ENTRADA', '🟢 Entrada'),
        ('SALIDA', '🔴 Salida'),
    ]
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=100, blank=True, help_text="Ej: Venta, Compra, Merma")
    
    # Opcional: Saber quién hizo el movimiento
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre}"