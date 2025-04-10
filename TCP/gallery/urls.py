from django.urls import path, include
from django.contrib import admin
from .views import paintingsList, tagSearch, home
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('paintingsList/',views.paintingsList,name = 'paintingList'),
    path('tag-search/', tagSearch, name='tag-search'),
    path('artists/',views.artists,name = 'artists'),

    path('manage/', views.manage_content, name='manage_content'),

]