from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,User

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
    #artist = models.ManyToManyField(Artist,related_name='artists')
    tags = models.ManyToManyField(Tag, related_name='paintings',blank=True,null=True)
    
    def __str__(self):
        return self.title


