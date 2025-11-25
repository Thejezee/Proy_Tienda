from django.contrib import admin
from django.urls import path
from core.views import lista_productos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lista_productos, name='inicio'),
]
