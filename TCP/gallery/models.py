from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    is_artist = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'gallery_user'
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name="gallery_user_set",
        related_query_name="gallery_user",
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="gallery_user_set",
        related_query_name="gallery_user",
    )
    


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


class Artist(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,  # Временно разрешаем NULL
        blank=True
    )
    biography  = models.TextField(blank=True)
    photoURL  = models.ImageField(upload_to='artists/', blank=True)

    def __str__(self):
        return self.user.username if self.user else "Unnamed Artist"
    
class Painting(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='paintings/')
    description = models.TextField(blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title