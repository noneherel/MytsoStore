from django.contrib import admin
from .models import Product, Categories, CategoryInCategories, GetCartItem, TelegramUsers
# Register your models here.
admin.site.register(Product)
admin.site.register(Categories)
admin.site.register(CategoryInCategories)
admin.site.register(GetCartItem)
admin.site.register(TelegramUsers)