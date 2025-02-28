from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import ArtistViewSet, TagViewSet, PaintingViewSet

router = DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'tags', TagViewSet)
router.register(r'paintings', PaintingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('gallery.urls')),
]