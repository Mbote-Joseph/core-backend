from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.auth.backends import ModelBackend


class SuperAdmin(AbstractBaseUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)
    id_number = models.CharField(max_length=50)
    role = models.CharField(max_length=50, default="superadmin")


    USERNAME_FIELD = 'email'

class Admin(AbstractBaseUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)
    id_number = models.CharField(max_length=50)
    building = models.ForeignKey('Building', on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=50, default="admin")

    USERNAME_FIELD = 'email'

class Visitor(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    id_number = models.CharField(max_length=50)

class Building(models.Model):
    name = models.CharField(max_length=100)
    superadmin = models.ForeignKey(SuperAdmin, on_delete=models.CASCADE, related_name='buildings')


class Floor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='floors')
    floor_number = models.IntegerField()


class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    is_office = models.BooleanField(default=False)

