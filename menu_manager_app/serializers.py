from rest_framework import serializers
from .models import Menu, Dish


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(MenuSerializer, self).to_representation(instance)
        representation['dishes'] = DishSerializer(instance.dishes.all(), many=True).data
        return representation
