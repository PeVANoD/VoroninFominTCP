from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gallery.urls')),  # Все остальные URL-адреса из приложения gallery
]