from django.db import models
from User.models  import Restaurant ,Customer
class Food(models.Model):
    name = models.CharField(max_length=255)
    category = (
        ("drink", "Drink"), 
        ("iranian_food", "Iranian_food"), 
        ("foreign_food", "Foreign_food"), 
    )
    price = models.DecimalField(decimal_places=2,max_digits=20 , null= True )
    ingredients = models.CharField(max_length=2048, null=True , blank=True)
    food_pic = models.ImageField(upload_to='Food_pics/', blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant,on_delete= models.CASCADE , related_name= 'food' )
    Type = models.CharField(choices=category,max_length=255, blank=True)
    def __str__(self) -> str:
        return self.name
    
class Order(models.Model):
    status = (
        ("InProgress", "InProgress"), 
        ("Completed", "Completed"), 
        ("Cancle", "Cancle"), 
        ("Ordered","Ordered") # before restaurant confirmation
        ("notOrdered","notOrdered")
    )
    status = models.CharField(choices = status , default= "notOrdered" )
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name="Orders")
    userId = models.ForeignKey(Customer,on_delete=models.DO_NOTHING,related_name="Orders")
    created_at = models.DateTimeField(auto_now_add= True)

class OrderItem(models.Model):
    food = models.ForeignKey(Food,on_delete=models.DO_NOTHING,related_name="orderItems")
    quantity = models.IntegerField()
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="orderItems")
    




    
