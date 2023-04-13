from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=255)
    # food_image = models.ImageField(null= True, blank= True)
    category = (
        ("drink", "Drink"), 
        ("iranian_food", "Iranian_food"), 
        ("foreign_food", "Foreign_food"), 
    )
    price = models.DecimalField(decimal_places=2,max_digits=20 , null= True )
    ingredients = models.CharField(max_length=2048, null=True , blank=True)
    # Food_pic = models.ImageField(upload_to='Food_pics/', blank=True, null=True)
    Type = models.CharField(choices=category,max_length=255, blank=True)
    def __str__(self) -> str:
        return self.name



    
