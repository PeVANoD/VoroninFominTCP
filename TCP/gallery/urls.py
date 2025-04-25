from django.urls import path
from django.contrib import admin
from django.http import HttpResponseForbidden
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .views import (
    home,
    paintingsList,
    tagSearch,
    artists,
    manage_content,
    auth_page,
    guest_page,
    
)

# Кастомный обработчик для админки
def admin_login_redirect(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('home')  # или на любую другую страницу
    return admin.site.login(request)

urlpatterns = [
    path('admin/login/', user_passes_test(lambda u: u.is_staff, login_url='home')(admin_login_redirect)),
    path('admin/', admin.site.urls),

    # Публичные эндпоинты
    path('', home, name='home'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Защищенные эндпоинты
    path('manage/', manage_content, name='manage_content'),

    # Остальные эндпоинты
    path('paintingsList/', paintingsList, name='paintingList'),
    path('tag-search/', tagSearch, name='tag-search'),
    path('artists/', artists, name='artists'),

    path('login/', views.custom_login, name='login'),
    path('register/', views.custom_register, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    path('guest/', guest_page, name='guest_page'),

    path('artist/', views.artist_dashboard, name='artist_dashboard'),
]