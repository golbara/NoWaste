from django.contrib.auth import get_user_model,logout
from rest_framework.permissions import BasePermission
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render, redirect
from rest_framework.viewsets import ModelViewSet , GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status ,generics,mixins,viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from .permissions import  IsAdminOrReadOnly
from rest_framework.decorators import action, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import *
from .models import *
from .filters import RestaurantFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class ChangePasswordView(generics.UpdateAPIView):
    # queryset = Restaurant.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    def put(self, request, *args, **kwargs):
        user = request.user
        if(user.id != self.kwargs['pk']):
            return Response({"message": "Unathorized!"},status=status.HTTP_401_UNAUTHORIZED)
        super().update(request, *args, **kwargs) 
        return Response({"message" :"Password changed successfully!"},status= status.HTTP_200_OK)


class RestaurantView(generics.RetrieveAPIView):

    def get_queryset(self):
        return Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'id'


# class RestaurantProfileView(generics.RetrieveUpdateAPIView):
#     def get_queryset(self):
#         return Restaurant.objects.get(self.kwargs['id'])
#     lookup_field = 'id'
#     serializer_class = RestaurantSerializer

class RestaurantProfileViewSet(viewsets.ViewSet):
    lookup_field = 'id'
    serializer_class = RestaurantSerializer
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.serializer_class(*args, **kwargs)
        kwargs['context'] = self.get_serializer_context()
        return serializer_class
    def get_serializer_context(self):
        return {'request': self.request}
    def get_object(self, id):
        try:
            return Restaurant.objects.get(id=id)
        except Restaurant.DoesNotExist:
            raise Response(status= status.HTTP_404_NOT_FOUND)
    def list(self, request):
        queryset = Restaurant.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        queryset = Restaurant.objects.get(id=id)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)
    def patch(self,request,id):
        instance = self.get_object(id= id)
        for key , value in request.data.items():
            setattr(instance,key,value)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

class RestaurantCustomerView(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'id'
    
class FoodViewSet(ModelViewSet):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()

    # @action(detail=True, methods=['patch'])
    def patch(self, request, id):
        instance = self.get_object(id= id)
        for key , value in request.data.items():
            setattr(instance,key,value)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class RestaurantSearchViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSearchSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RestaurantFilter
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name']
    ordering_fields = ['rate', 'discount', 'name', 'date_of_establishment']

    def get_serializer_context(self):
        return {'request': self.request}


# class CreateOrderViewSet(ModelViewSet):
# class OrderViewSet(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin, GenericViewSet):
class OrderViewSet(mixins.CreateModelMixin,mixins.RetrieveModelMixin):
    queryset = Order.objects.prefetch_related('orderItems__food').all()
    serializer_class = GetOrderSerializer

    # def get_serializer(self, *args, **kwargs):
    #     return GetOrderSerializer
    #     if self.request.method == "GET":
    #         return GetOrderSerializer

    # def create(self, request):
    #     pass

    # def retrieve(self, request, pk=None):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)


    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass


class OrderItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        return OrderItemSerializer
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'order_id': self.kwargs['id']}

    def get_queryset(self):
        return OrderItem.objects \
            .filter(order_id=self.kwargs['id']) \
            .select_related('food')
