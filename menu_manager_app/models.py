from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Dish(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    price = models.FloatField()
    preparation_time = models.DurationField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    vegetarian = models.BooleanField(blank=False, default=False)


class Menu(models.Model):
    name = models.CharField(unique=True, max_length=80)
    dishes = models.ManyToManyField(Dish)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
