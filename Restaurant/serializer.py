from decimal import Decimal
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from User.models import Restaurant ,Customer, RestaurantManager
from User.serializers import MyAuthorSerializer
from .models import *

class RestaurantSerializer(serializers.ModelSerializer):
    # def Menu(self):
    # def Menu(self,obj):
    #     foods = Food.objects.filter(restaurant=obj)
    #     serializer = FoodSerializer(foods, many=True)
    #     return serializer.data
    # menu = serializers.SerializerMethodField(method_name= 'Menu')  

    class Meta:
        model = Restaurant
        address = serializers.CharField(source = 'address')
        fields = ('number','name','address','restaurant_image','rate','discount','date_of_establishment','description','restaurant_image','id')

        extra_kwargs = {
            'menu': {'read_only': True},
            'address': {'required': False},
            'name' : {'required': False},
        }
    
    def validate_email(self, new_email):
        user = self.context['request'].user
        if Restaurant.objects.exclude(pk=user.pk).filter(email=new_email).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return new_email


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.number = validated_data.get('number', instance.number)
        instance.address = validated_data.get('address', instance.address)
        instance.date_of_establishment = validated_data.get('date_of_establishment', instance.date_of_establishment)
        instance.description = validated_data.get('description', instance.description)
        instance.restaurant_image = validated_data.get('restaurant_image', instance.restaurant_image)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.save()
        return instance
    


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True,source = 'password')

    class Meta:
        model = RestaurantManager
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        #  user = self.context['request'].user

        if not user.is_authenticated:
            raise serializers.ValidationError({"authorize": "You must be logged in to perform this action."})

        if user.pk != self.instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class RestaurantSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'discount', 'rate', 'date_of_establishment', 'id', 'description', 'restaurant_image']
        lookup_field = 'id'

class FoodFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['name', 'price', 'ingredients', 'food_pic', 'restaurant','type']
        lookup_field = 'id'

class FoodSerializer(serializers.ModelSerializer):
    restaurant_id = serializers.IntegerField(read_only = False)
    class Meta :
        model = Food
        # fields = '__all__'
        fields = ['name','price','ingredients','food_pic','restaurant_id','type','id']


class RestaurantManagerSerializer(serializers.ModelSerializer):
    restaurants = RestaurantSerializer(many = True, read_only=True)
    class Meta:
        model = RestaurantManager
        fields = ['id', 'name','email','restaurants','number', 'manager_image']

    def create(self, validated_data):
        restaurants_data = validated_data.pop('restaurants',[])
        manager = RestaurantManager.objects.create(**validated_data)
        for res_data in restaurants_data:
            Restaurant.objects.create(manager = manager, **res_data)
        return manager
    
    def update(self, instance, validated_data):
        restaurants_data = validated_data.pop('restaurants', [])
        for res_data in restaurants_data:
            res_id = res_data.get('id', None)
            if res_id:
                restaurant = instance.restaurants.filter(id=res_id).first()
                if restaurant:
                    restaurant.name = res_data.get('name', restaurant.name)
                    restaurant.save()
                else:
                    Restaurant.objects.create(manager=instance, **res_data)
            else:
                Restaurant.objects.create(manager=instance, **res_data)
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.number = validated_data.get('number', instance.number)
        instance.manager_image = validated_data.get('manager_image', instance.manager_image)
        instance.save()
        return instance
class SimpleFoodSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Food
        # fields = ('name')
        fields = ['name','price']

class OrderItemSerializer(serializers.ModelSerializer):
    def get_name_and_price(self,orderitem):
        return SimpleFoodSerializer(orderitem.food).data
    name_and_price = serializers.SerializerMethodField()
    class Meta : 
        model = OrderItem
        fields = ('quantity','name_and_price')

class GetOrderSerializer(serializers.ModelSerializer):
    def get_Subtotal_Grandtotal_discount(self, order:Order):
        quantities = []
        price = []
        discount = 0
        Grandtotal = 0
        Subtotal = 0
        for item in order.orderItems.all():
            price.append(item.quantity * item.food.price)
            quantities.append(item.quantity)
        Subtotal = sum(price)
        Grandtotal = Subtotal
        if order.restaurant.discount == 0:
            discount = 0
        elif sum(quantities) < order.restaurant.purches_counts:
            discount = 0
        else : 
            discount = order.restaurant.discount
        if (discount != 0):
            Grandtotal =(1-discount) * Subtotal
        return Subtotal,Grandtotal,discount

    def get_userAddress(self,order :Order):
        return order.userId.address
    
    orderItems = OrderItemSerializer(many=True, read_only=True)
    Subtotal_Grandtotal_discount = serializers.SerializerMethodField()
    userAddress = serializers.SerializerMethodField()

    class Meta : 
        model = Order
        fields = ('id','orderItems','userAddress','Subtotal_Grandtotal_discount')

        extra_kwargs = {
        'orderItems': {'read_only': True},
        'discount': {'read_only': True},
        'total_price': {'read_only': True}
        }

class CreateOrderSerializer(serializers.ModelSerializer):
    userId_id = serializers.IntegerField()
    restaurant_id = serializers.IntegerField()
    class Meta : 
        model = Order
        fields = ['userId_id','restaurant_id']
class SimpleRestaurantSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Restaurant
        fields = ['name','address','logo','number']

class CustomerViewOrderSerializer(serializers.ModelSerializer):
    def get_orderDetails(self,order):
        return GetOrderSerializer(order).data
    def get_restaurantDetails(self,order):
        return SimpleRestaurantSerializer(order.restaurant).data
    orderDetails = serializers.SerializerMethodField()  # Embedding ParentSerializer in ChildSerializer
    restaurantDetails = serializers.SerializerMethodField()
    status = serializers.CharField()

    class Meta : 
        model = Order
        fields = ['orderDetails','restaurantDetails','status']

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta :
        model = Customer
        fields = ['name','phone_number','address','username']
class RestaurantOrderViewSerializer(serializers.ModelSerializer):
    def get_orderDetails(self,order):
        return GetOrderSerializer(order).data
    def get_userDetails(self,order):
        return SimpleUserSerializer(order.userId).data
    orderDetails = serializers.SerializerMethodField()  # Embedding ParentSerializer in ChildSerializer
    userDetails = serializers.SerializerMethodField()
    status = serializers.CharField()

    class Meta : 
        model = Order
        fields = ['orderDetails','userDetails','status']


class CommentSerializer(serializers.ModelSerializer):
    # writer_username = serializers.CharField( required=False, validators=[])
    # restaurant_name = serializers.CharField( required=False, validators=[])
    writer_username = serializers.CharField(source='writer.username', read_only=True)
    created_at = serializers.DateField(required=False, read_only=True)
    class Meta : 
        model = Comment
        fields = ['text', 'writer_username', 'created_at']
    # def create(self, validated_data):
        # writer_username = validated_data.pop('writer_username',None)
        # restaurant_name = validated_data.pop('restaurant_name',None)
        # return super().create(validated_data)
