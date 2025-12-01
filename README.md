# Sistema de Control de Inventario - Mercado / Minimarket  
**Django + MySQL (XAMPP)**

Proyecto completo de gestión de productos, stock físico, movimientos de entrada/salida y proveedores.  
Base de datos real incluida con ejemplo funcional (Coca Cola 3L, etc.).

## Estructura de la base de datos (db_mercado)

- `core_producto` → Productos (nombre, SKU único, precio, stock mínimo, imagen)
- `core_stock` → Cantidad real y ubicación física (Refrigerador 1, Estante A, etc.)
- `core_movimientostock` → Registro completo de entradas y salidas (compra, venta, merma, ajuste)
- `core_proveedor` → Datos de proveedores
- Tablas de Django (auth_user, django_admin_log, etc.) → Admin y usuarios

## Requisitos
- Python 3.9+
- MySQL (recomendado XAMPP)
- Git (opcional)

## Instalación y ejecución (PASO A PASO)

### 1. Descomprimir o clonar el proyecto
```bash
Creacion del enteorno virtual:
python -m venv venv
.venv\Scripts\activate
Instalar dependencias
----------------
pip install -r requirements.txt
----------------
Ejecutar migraciones

----------------
python manage.py makemigrations
python manage.py migrate


Ejecucion final
python manage.py runserver
