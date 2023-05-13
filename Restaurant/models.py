from django.db import models
from User.models  import Restaurant
class Food(models.Model):
    name = models.CharField(max_length=255)
    category = (
        ("drink", "Drink"), 
        ("iranian_food", "Iranian_food"), 
        ("foreign_food", "Foreign_food"), 
    )
    price = models.DecimalField(decimal_places=2,max_digits=20 , null= True )
    ingredients = models.CharField(max_length=2048, null=True , blank=True)
    food_pic = models.TextField(blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant,on_delete= models.CASCADE , related_name= 'food' )
    Type = models.CharField(choices=category,max_length=255, blank=True)
    def __str__(self) -> str:
        return self.name


