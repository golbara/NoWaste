from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Restaurant(models.Model):

    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    discount = models.DecimalField(max_digits=2, decimal_places=2, blank=True)
    purches_counts =models.IntegerField(blank= True)
    def __str__(self) -> str:
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=255)
    restaurants = models.ManyToManyField(Restaurant, related_name="food")
    category = (
        ("drink", "Drink"), 
        ("iranian_food", "Iranian_food"), 
        ("foreign_food", "Foreign_food"), 
    )
    Type = models.CharField(choices=category,max_length=255)
    def __str__(self) -> str:
        return self.name
    
class Food_Specifics(models.Model):
    price = models.DecimalField(decimal_places=2,max_digits=20)
    ingredients = models.CharField(max_length=1024, null=True)
    FoodID = models.ForeignKey(Food, on_delete=models.CASCADE)
    # Food_pic = models.ImageField(upload_to='Food_pics/', blank=True, null=True)
    ResID = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('FoodID', 'ResID',)
    