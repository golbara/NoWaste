from django.db import models
from User.models  import Restaurant ,Customer
from uuid import uuid4

class Food(models.Model):
    name = models.CharField(max_length=255)
    category = (
        ("Drink", "Drink"), 
        ("Iranian", "Iranian"), 
        ("Foreign", "Foreign"), 
    )
    price = models.DecimalField(decimal_places=2,max_digits=20 , null= True )
    ingredients = models.CharField(max_length=2048, null=True , blank=True)
    food_pic = models.TextField(blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant,on_delete= models.CASCADE , related_name= 'food' )
    type = models.CharField(choices=category,max_length=255, blank=True)
    def __str__(self) -> str:
        return self.name
    
class Order(models.Model):
    status = (
        ("InProgress", "InProgress"), 
        ("Completed", "Completed"), 
        ("Cancled", "Cancled"), 
        ("Ordered","Ordered") ,# before restaurant confirmation
        ("notOrdered","notOrdered"),
    )
    id = models.UUIDField(primary_key=True, default=uuid4)
    status = models.CharField(choices = status , default= "notOrdered", max_length= 255)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name="Orders")
    userId = models.ForeignKey(Customer,on_delete=models.DO_NOTHING,related_name="Orders")
    created_at = models.DateTimeField(auto_now_add= True)
    def __str__(self) -> str:
        return "user: " + str(self.userId) + " - order id: " + str(self.id)
    # class Meta:
    #     unique_together = ('userId', 'restaurant',)

class OrderItem(models.Model):
    food = models.ForeignKey(Food,on_delete=models.DO_NOTHING,related_name="orderItems")
    quantity = models.IntegerField(default= 0)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="orderItems")

class Comment(models.Model):
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name="comments")
    writer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    text = models.CharField(max_length=512, default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self) -> str:
        return str(self.writer.name) + " "+  str(self.restaurant.name)
