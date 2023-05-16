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
from .filters import RestaurantFilter , FoodFilter
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


class RestaurantView(viewsets.ViewSet):

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
    # queryset = Food.objects.all()
    def get_queryset(self):
        print(self.kwargs)
        return Food.objects.filter(restaurant_id=self.kwargs['restaurant__id'])


    def get_serializer_context(self):
        return {'restaurant_id': self.kwargs['restaurant__id']}
    # @action(detail=True, methods=['patch'])
    def patch(self, request, id):
        instance = self.get_object(id= id)
        for key , value in request.data.items():
            setattr(instance,key,value)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class ManagerFoodAPIView(generics.ListAPIView):
    serializer_class = FoodSerializer
    def get_queryset(self):
        print(self.kwargs)
        return Food.objects.filter(restaurant_id=self.kwargs['restaurant_id'])


    def get_serializer_context(self):
        print(self.kwargs)
        return {'restaurant_id': self.kwargs['restaurant_id']}

class ManagerFoodViewSet(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FoodSerializer
    lookup_field = 'pk'
    def get_queryset(self):
        print(self.kwargs)
        return Food.objects.filter(restaurant_id=self.kwargs['restaurant_id'])


    def get_serializer_context(self):
        print(self.kwargs)
        return {'restaurant_id': self.kwargs['restaurant_id']}

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
    

class FilterFoodViewSet(ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodFilterSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FoodFilter
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name']
    ordering_fields = ['price', 'name']

    def get_serializer_context(self):
        return {'request': self.request}


class RestaurantManagerListCreateView(generics.ListCreateAPIView):
    queryset = RestaurantManager.objects.all()
    serializer_class = RestaurantManagerSerializer

class RestaurantManagerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestaurantManager.objects.all()
    serializer_class = RestaurantManagerSerializer

class RestaurantManagerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestaurantManager.objects.all()
    serializer_class = RestaurantManagerSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['manager'] = self.get_object()
        return context
    
class RestaurantManagerRestaurantListView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        try:
            mang = RestaurantManager.objects.get(id=self.kwargs['manager_id'])
        except RestaurantManager.DoesNotExist:
            return Response("There is not any restaurant manager with the given id" , status=status.HTTP_404_NOT_FOUND)
        return self.queryset.filter(manager = mang)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['manager'] = RestaurantManager.objects.get(pk = self.kwargs['manager_id'])
        return context
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                mang = RestaurantManager.objects.get(id=self.kwargs['manager_id'])
            except RestaurantManager.DoesNotExist:
                return Response("There is not any restaurant manager with the given id" , status=status.HTTP_404_NOT_FOUND)
            serializer.save(manager = mang)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class RestaurantManagerRestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['manager'] = RestaurantManager.objects.get(pk=self.kwargs['manager_id'])
        return context


# class CreateOrderViewSet(ModelViewSet):
class OrderViewSet(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin, GenericViewSet):
    # serializer_class = GetOrderSerializer
    current_user_id = None
    def get_queryset(self):
        print(self.kwargs)
        # current_user_id = self.request.user.id
        # print(current_user_id)
        return Order.objects.filter(restaurant_id=self.kwargs['restaurant__id'] ,userId_id = self.current_user_id)
    
    def get_serializer_class(self, *args, **kwargs):
        if (self.request.method == 'GET'):
            return GetOrderSerializer
        if(self.request.method == 'POST'):
            return CreateOrderSerializer

    def get_serializer_context(self):
        return {'restaurant_id': self.kwargs['restaurant__id']}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # print(serializer.data)
        serializer.save()
        self.current_user_id = serializer.data['userId_id']
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
