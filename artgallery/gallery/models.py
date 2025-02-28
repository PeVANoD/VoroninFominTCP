from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class ArtistManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)


class Artist(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    biography = models.TextField(blank=True)
    photo = models.ImageField(upload_to='artists/', blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Django автоматически хеширует пароли
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = ArtistManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class Painting(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    imageURL = models.URLField()
    description = models.TextField(blank=True)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE, related_name='paintings')
    tags = models.ManyToManyField('Tag', related_name='paintings')
    
    def __str__(self):
        return self.title
