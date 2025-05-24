from django.urls import path, include
from django.contrib import admin
from .views import paintingsList, tagSearch, home
from . import views

urlpatterns = [
<<<<<<< Updated upstream
=======
    path('admin/login/', user_passes_test(lambda u: u.is_staff, login_url='home')(admin_login_redirect)),

    # Публичные эндпоинты
>>>>>>> Stashed changes
    path('', home, name='home'),
    path('paintingsList/',views.paintingsList,name = 'paintingList'),
    path('tag-search/', tagSearch, name='tag-search'),
    path('artists/',views.artists,name = 'artists'),

    path('manage/', views.manage_content, name='manage_content'),

]