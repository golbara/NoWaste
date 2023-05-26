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
from rest_framework.renderers import JSONRenderer
from django.db.models import Q
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
    

class ManagerFoodListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = FoodSerializer
    def get_queryset(self):
        print(self.kwargs)
        return Food.objects.filter(restaurant_id=self.kwargs['restaurant_id'])


    def get_serializer_context(self):
        print(self.kwargs)
        return {'restaurant_id': self.kwargs['restaurant_id']}

    def create(self, request, *args, **kwargs):
        # instance = request.data
        # instance['restaurant_id'] = self.kwargs['restaurant_id']
        # print(instance)
        # serializer = FoodSerializer(data= instance)
        serializer = FoodSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

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


class OrderAPIView(generics.RetrieveUpdateAPIView,generics.CreateAPIView):
    serializer_class = GetOrderSerializer
    lookup_field = 'pk'
    def get_queryset(self):
        return Order.objects.filter(restaurant_id=self.kwargs['restaurant_id'] ,userId_id = self.kwargs['userId']).prefetch_related('orderItems').select_related('userId').select_related('restaurant')
    
    def get_serializer_class(self, *args, **kwargs):
        return GetOrderSerializer

    def get_serializer_context(self):
        return {'restaurant_id': self.kwargs['restaurant_id'],'userId_id' : self.kwargs['userId']}
    
    def retrieve(self, request, *args, **kwargs):
        instance =  self.get_queryset().filter(restaurant_id=self.kwargs['restaurant_id'],userId_id = self.kwargs['userId']).exclude(Q(status='Completed') | Q(status='Ordered'))
        serializer = None
        if (instance.count() == 0) :
            print("hiii")
            instance = Order.objects.create(restaurant_id=self.kwargs['restaurant_id'],userId_id = self.kwargs['userId'])
            serializer = self.get_serializer(instance)
        else :
            serializer = self.get_serializer(instance,many = True)
        return Response(serializer.data)
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


def add_to_Order(request, *args, **kwargs):
    order  =  Order.objects.filter(restaurant_id=kwargs['restaurant_id'],userId_id = kwargs['userId'],status = 'notOrdered').first()
    if(order is None):
        order = Order.objects.create(restaurant_id=kwargs['restaurant_id'],userId_id = kwargs['userId'])
        instance = OrderItem.objects.create(food_id = kwargs['food_id'], order_id = order.id)
    else :
        instance = OrderItem.objects.filter(food_id = kwargs['food_id'], order_id = order.id).first()
        if (instance is None):
            instance = OrderItem.objects.create(food_id = kwargs['food_id'], order_id = order.id)
    instance.quantity = instance.quantity+ 1
    instance.save()
    
    serializer = OrderItemSerializer(instance)
    serialized_data = serializer.data

    content = JSONRenderer().render(serialized_data)
    return HttpResponse(content, content_type='application/json')

def remove_from_Order(request, *args, **kwargs):
    order  =  Order.objects.filter(restaurant_id=kwargs['restaurant_id'],userId_id = kwargs['userId'],status = 'notOrdered').first()
    if(order is None):
        order = Order.objects.create(restaurant_id=kwargs['restaurant_id'],userId_id = kwargs['userId'])
        instance = OrderItem.objects.create(food_id = kwargs['food_id'], order_id = order.id)
    else :
        instance = OrderItem.objects.filter(food_id = kwargs['food_id'], order_id = order.id).first()
        if (instance is None):
            instance = OrderItem.objects.create(food_id = kwargs['food_id'], order_id = order.id)
    instance.quantity = instance.quantity- 1
    if(instance.quantity < 0) :
        instance.quantity = 0 
    instance.save()
    
    serializer = OrderItemSerializer(instance)
    serialized_data = serializer.data

    content = JSONRenderer().render(serialized_data)
    return HttpResponse(content, content_type='application/json')

class OrderItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        return OrderItemSerializer

    def get_serializer_context(self):
        return {'order_id': self.kwargs['id']}

    def get_queryset(self):
        return OrderItem.objects \
            .filter(order_id=self.kwargs['id']) \
            .select_related('food')
class CustomerOrderViewAPI(generics.ListAPIView):
    def get_serializer_class(self):
        return CustomerViewOrderSerializer

    def get_queryset(self):
        return Order.objects.filter(userId_id=self.kwargs['user_id']).select_related('restaurant')
    
class RestaurantOrderViewAPI(generics.ListAPIView):
    serializer_class = RestaurantOrderViewSerializer

    def get_queryset(self):
        return Order.objects.filter(restaurant_id=self.kwargs['restaurant_id']).select_related('userId')

class UpdateOrderStatusAPI(generics.UpdateAPIView):
    def get_serializer_class(self, *args, **kwargs):
        return UpdateOrderSerializer
    def get_queryset(self):
        return Order.objects.filter(id = self.kwargs['order_id'])
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.save()
        return Response(serializer.data)
    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)


class CommentAPI(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        writer = Customer.objects.get(id = kwargs['user_id'])
        restaurant = Restaurant.objects.get(id = kwargs['restaurant_id'])
        # serializer.initial_data['writer_username'] = writer.username
        # serializer.initial_data['restaurant_name'] = restaurant.name
        if serializer.is_valid(raise_exception=True):
            new_comment, created = Comment.objects.get_or_create(writer = writer, restaurant=restaurant)
            
            new_comment.text = serializer.validated_data['text']
            # serializer.save()
            new_comment.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        serializer = CommentSerializer()
        writer = Customer.objects.get(id = kwargs['user_id'])
        restaurant = Restaurant.objects.get(id = kwargs['restaurant_id'])
        try:
            comment = Comment.objects.get(writer=writer, restaurant=restaurant)
            return Response({'comment': comment.text}, status=status.HTTP_200_OK)
        except:
            return Response(serializer.data, status=status.HTTP_200_OK)

class RestaurantCommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return Comment.objects.filter(restaurant_id=restaurant_id)
