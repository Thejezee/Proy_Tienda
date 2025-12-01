from django.contrib import admin
from django.urls import path, include
from core import views  # <--- ESTO ES LO QUE FALTABA PARA QUE FUNCIONE

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # --- RUTAS PRINCIPALES ---
    path('', views.pagina_inicio, name='inicio'),          # Raíz -> Bienvenida
    path('inventario/', views.lista_productos, name='inventario'), # Dashboard
    
    # --- OPERACIONES ---
    path('movimiento/nuevo/', views.registrar_movimiento, name='registrar_movimiento'),
    path('historial/', views.historial_movimientos, name='historial'),
    
    # --- ACCIONES CRUD ---
    path('producto/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
]