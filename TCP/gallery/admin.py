from django.contrib import admin
from .models import Painting, Tag,Artist
# Register your models here.

admin.site.register(Painting)
admin.site.register(Tag)
admin.site.register(Artist)
