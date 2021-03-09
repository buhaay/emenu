from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from .models import Menu, Dish
from .serializers import MenuSerializer, DishSerializer


class MenuView(ModelViewSet, generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Menu.objects.all().prefetch_related("dishes")
    serializer_class = MenuSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["name", "total_dishes"]

    @action(detail=False, permission_classes=[AllowAny])
    def get_not_empty(self, request):
        carts = Menu.objects.exclude(dishes__isnull=True)
        carts_serializer = MenuSerializer(carts, many=True)
        return Response(carts_serializer.data)

    def get_queryset(self):
        name = self.request.query_params.get("name", None)
        queryset = Menu.objects.all()
        if name is not None:
            queryset = queryset.filter(name=name)
            return queryset
        return queryset

    @action(detail=False, permission_classes=[AllowAny])
    def recent_carts(self, request):
        recent_carts = Menu.objects.all().order_by("-created")
        page = self.paginate_queryset(recent_carts)
        if page is not None:
            cart_serializer = self.get_serializer(recent_carts, many=True)
            return self.get_paginated_response(cart_serializer.data)

        cart_serializer = self.get_serializer(recent_carts, many=True)
        return Response(cart_serializer.data)

    @action(detail=False, permission_classes=[AllowAny])
    def recent_updated_carts(self, request):
        recent_carts = Menu.objects.all().order_by("-updated")
        page = self.paginate_queryset(recent_carts)
        if page is not None:
            cart_serializer = self.get_serializer(recent_carts, many=True)
            return self.get_paginated_response(cart_serializer.data)

        cart_serializer = self.get_serializer(recent_carts, many=True)
        return Response(cart_serializer.data)


class MenuDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete cart.
    """

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class DishView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
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


class DishDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete dish.
    """

    queryset = Dish.objects.all()
    serializer_class = DishSerializer
