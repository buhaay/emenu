from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Menu, Dish
from .serializers import MenuSerializer, DishSerializer


class MenuView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """
        Return list of all carts.
        """
        carts = Menu.objects.all()
        carts_serializer = MenuSerializer(carts, many=True)
        return Response(carts_serializer.data)

    def post(self, request):
        """
        Create new cart.
        """
        carts_serializer = MenuSerializer(data=request.data)
        if carts_serializer.is_valid():
            carts_serializer.save()
            return Response(carts_serializer.data, status=status.HTTP_201_CREATED)
        return Response(carts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DishView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return list of all dishes.
        """
        dishes = Dish.objects.all()
        dishes_serializer = DishSerializer(dishes, many=True)
        return Response(dishes_serializer.data)

    def post(self, request):
        """
        Create new dish.
        """
        dishes_serializer = DishSerializer(data=request.data)
        if dishes_serializer.is_valid():
            dishes_serializer.save()
            return Response(dishes_serializer.data, status=status.HTTP_201_CREATED)
        return Response(dishes_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
