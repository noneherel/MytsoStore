from django.db import models
from django.contrib.auth.models import User
import json
import telebot
# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='api/categories/', blank=True)
    description = models.TextField()
    
    def __str__(self):
        return self.name
class CategoryInCategories(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='api/CategoryInCategories/', blank=True)
    description = models.TextField()
    
    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='api/products/', blank=True)
    sells = models.IntegerField(default=0)
    categ = models.ForeignKey(Categories, on_delete=models.CASCADE, default=None, blank=True,null=True)
    categ2 = models.ForeignKey(CategoryInCategories, on_delete=models.CASCADE, default=None, blank=True,null=True)
    popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'item', 'quantity')
class GetCartItem(models.Model):
    IDs = models.CharField(default='',max_length=200)
    # Id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    subtotoal = models.CharField(max_length=200, default='')
    username = models.CharField(max_length=25, default='')
    
class TelegramUsers(models.Model):
    user = models.CharField(max_length=50, default='')
    def __str__(self):
        return self.user