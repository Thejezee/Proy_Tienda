from django.core.management.base import BaseCommand
from core.models import Producto, Proveedor, Stock
import random

class Command(BaseCommand):
    help = 'Carga 500 productos de prueba masivamente'

    def handle(self, *args, **kwargs):
        self.stdout.write("🏭 Iniciando carga industrial de 500 productos...")

        # 1. PROVEEDORES (Más variedad)
        proveedores_data = [
            'Coca Cola', 'Pepsi', 'Arcor', 'Nestlé', 'Bimbo', 'Pil', 'Gloria', 
            'Fanguito', 'Kris', 'Delizia', 'San Gabriel', 'Venado', 'Sofia', 
            'Aceite Fino', 'Huggies', 'Colgate'
        ]
        lista_provs = []
        
        for nombre in proveedores_data:
            prov, created = Proveedor.objects.get_or_create(
                nombre=nombre,
                defaults={'telefono': f'7{random.randint(1000000, 9999999)}', 'email': f'ventas@{nombre.lower().replace(" ", "")}.com'}
            )
            lista_provs.append(prov)

        # 2. PRODUCTOS BASE
        nombres_base = [
            'Gaseosa', 'Galletas', 'Leche', 'Yogurt', 'Pan', 'Chocolate', 
            'Agua', 'Jugo', 'Cereal', 'Aceite', 'Arroz', 'Fideo', 
            'Atún', 'Café', 'Mermelada', 'Shampoo', 'Jabón', 'Pañales',
            'Detergente', 'Helado', 'Queso', 'Mantequilla', 'Salsa de Tomate',
            'Mayonesa', 'Mostaza', 'Refresco', 'Vino', 'Cerveza'
        ]

        # 3. VARIANTES (Para multiplicar combinaciones sin repetir)
        variantes = [
            'Clásico', 'Premium', 'Light', 'Sin Azúcar', 'Familiar', 
            'Pequeño', 'Grande', 'Pack 3', 'Oferta', 'Extra', 
            'Vainilla', 'Chocolate', 'Frutilla', '1 Litro', '500ml',
            '2 Kilos', 'Barra', 'Lata', 'Botella'
        ]

        # 4. GENERADOR MASIVO
        contador = 0
        intentos = 0
        
        # Seguir intentando hasta tener 500 o que se nos acaben las ideas
        while contador < 500 and intentos < 2000:
            intentos += 1
            
            base = random.choice(nombres_base)
            prov = random.choice(lista_provs)
            variante = random.choice(variantes)
            
            # Nombre Profesional: Ej "Leche Pil 1 Litro"
            nombre_final = f"{base} {prov.nombre} {variante}"
            
            # Solo creamos si NO existe (para evitar errores)
            if not Producto.objects.filter(nombre=nombre_final).exists():
                precio_base = random.randint(5, 80)
                sku = f"SKU-{random.randint(100000, 999999)}"
                
                if not Producto.objects.filter(sku=sku).exists():
                    prod = Producto.objects.create(
                        nombre=nombre_final,
                        sku=sku,
                        precio=precio_base + random.choice([0.50, 0.90, 0.00, 0.20]), 
                        min_stock=random.randint(5, 20),
                        proveedor=prov
                    )
                    
                    # Stock Inicial
                    Stock.objects.create(
                        producto=prod,
                        ubicacion=random.choice(['Estante A', 'Estante B', 'Bodega Central', 'Refrigerador 1', 'Refrigerador 2', 'Mostrador']),
                        cantidad=random.randint(0, 150)
                    )
                    
                    contador += 1
                    if contador % 50 == 0:
                        self.stdout.write(f" ... {contador} productos listos")

        self.stdout.write(self.style.SUCCESS(f"✅ ¡MISIÓN CUMPLIDA! Se cargaron {contador} productos al sistema."))