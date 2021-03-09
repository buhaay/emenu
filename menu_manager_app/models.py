from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Count


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

    def __str__(self):
        return f"Dish name: {self.name}. Description: {self.description}. Price: {self.price}"


class MenuManager(models.Manager):
    def get_queryset(self):
        return super(MenuManager, self).get_queryset().annotate(total_dishes=Count('dishes'))


class Menu(models.Model):
    name = models.CharField(unique=True, max_length=80)
    dishes = models.ManyToManyField(Dish, blank=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = MenuManager()
