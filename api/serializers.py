from rest_framework.serializers import ModelSerializer
from .models import Categories, Product, Cart, CartItem, CategoryInCategories, GetCartItem
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    def validate_email(self, email):
        # Check if a user with the provided email already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError("An email already exists.")
        return email
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        user.is_active = False
        user.save()
        return user
    
    
class LoginSerializer(serializers.Serializer):
    # class Meta:
    #     model = User
    #     fields = ('username', 'password')
        
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    # def validateLogIn(self, validated_data):
    #     user = authenticate(username=validated_data['username'], password=validated_data['password'])
        
    #     if not user is None:
    #         return user
    #     else:
    #         raise ValidationError({"invalid": "username or password is wrong"})

#another way:

# class LoginSerializer(serializers.Serializer):
# 	class Meta:
# 		model = User
# 		fields = ('username', 'password')
# 	##
# 	def check_user(self, clean_data):
# 		user = authenticate(username=clean_data['username'], password=clean_data['password'])
# 		if not user is None:
# 			raise ValidationError('user not found')
# 		return user
class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
class CategoryInCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryInCategories
        fields = '__all__'
        
class CartItemSerializer(serializers.ModelSerializer):
    item = serializers.CharField(source='item.name')
    
    class Meta:
        model = CartItem
        fields = ['item', 'quantity']
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']
class GetCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetCartItem
        fields = ['subtotoal', 'IDs', 'username']