from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Product, Categories, Cart, CartItem, CategoryInCategories, GetCartItem, TelegramUsers
from .serializers import RegisterSerializer, LoginSerializer, ProductSerializer, CategoriesSerializer, CategoryInCategoriesSerializer, GetCartSerializer
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated 
from rest_framework.request import Request
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
import telebot
from .tokens import create_jwt_pair_for_user
# from .tokens import create_jwt_pair_for_user

# Create your views here.
class PopularList(generics.ListCreateAPIView):
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
class ProductsList(generics.ListCreateAPIView):
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs= super().get_queryset()
        category = self.request.GET['category']
        category= Categories.objects.get(id = category)
        qs=qs.filter(categ=category)
        return qs
class ProductsList2(generics.ListCreateAPIView):
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs= super().get_queryset()
        category = self.request.GET['categorin']
        category= CategoryInCategories.objects.get(id = category)
        qs=qs.filter(categ2=category)
        return qs
class ProductList(generics.ListCreateAPIView):
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs= super().get_queryset()
        category = self.request.GET['category']
        # product = self.request.GET['product']
        category= Categories.objects.get(id = category)
        # product= Product.objects.get(id = product)
        qs=qs.filter(categ=category)
        return qs
    def get(self, request, *args, **kwargs):
        # Check if product_id is present in the URL
        product_id = self.request.GET.get('product_id')

        if product_id:
            try:
                # Retrieve and return the specific product
                product = Product.objects.get(id=product_id)
                serializer = self.serializer_class(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Continue with the default behavior if no product_id is provided
        return super().get(request, *args, **kwargs)
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCreate(generics.CreateAPIView):
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDelete(generics.DestroyAPIView):
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductUpdate(generics.UpdateAPIView):
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class SignUpView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        data = request.data
        
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            serializer.save()
            response = {"message": "User Created Successfully", "data": serializer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoginSerializer
    
    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:

            tokens = create_jwt_pair_for_user(user)

            response = {"message": "Login Successfull", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid username or password"})

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)
    
class UserLogout(APIView):
    permission_classes = ()

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
class DeleteUser(APIView):
    permission_classes = ()
    def post(self, request):
        if request:
            print(request)
            u = User.objects.get(username='abcd');u.delete();print('user has been deleted');
            return Response(status=status.HTTP_200_OK)
        
        
        
        
class CategoriesListView(APIView):
    """
    List all categories, or create a new Categories.
    """
    permission_classes = []
    def get(self, request, format=None):
        categories = Categories.objects.all()
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CategoryInCategoriesListView(APIView):
    """
    List all categories, or create a new Categories.
    """
    permission_classes = []
    def get(self, request, format=None):
        categories = CategoryInCategories.objects.all()
        serializer = CategoryInCategoriesSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategoryInCategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoriesDetailView(APIView):
    permission_classes = []
    """
    Retrieve, update or delete a Categories instance.
    """
    def get_object(self, pk):
        return get_object_or_404(Categories, pk=pk)

    def get(self, request, pk, format=None):
        Categories = self.get_object(pk)
        serializer = CategoriesSerializer(Categories)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Categories = self.get_object(pk)
        serializer = CategoriesSerializer(Categories, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Categories = self.get_object(pk)
        Categories.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class CategoriesDetailView2(APIView):
    permission_classes = []
    """
    Retrieve, update or delete a Categories instance.
    """
    def get_object(self, pk):
        return get_object_or_404(CategoryInCategories, pk=pk)

    def get(self, request, pk, format=None):
        Categories = self.get_object(pk)
        serializer = CategoryInCategoriesSerializer(Categories)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Categories = self.get_object(pk)
        serializer = CategoryInCategoriesSerializer(Categories, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Categories = self.get_object(pk)
        Categories.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class CategoriesCreateView(generics.CreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
bot = telebot.TeleBot('6344087091:AAE0FO_nDmmWb6km1GMzqelX9ViDX2z7deo')
class HandleCart(APIView):
    permission_classes = []
    serializer_class = GetCartSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = GetCartSerializer(data=data)
        
        # print(serializer)
        if serializer.is_valid():
            d = {}
            St = serializer.data['subtotoal']
            phoneNumber= serializer.data['username']
            toList = serializer.data['IDs'].split(',')
            num = 1
            l = ['980720808','1626922754']
            for i in toList:
                getProduct = Product.objects.get(id=i)
                d[f'اسم المنتج {num}'] = getProduct.name
                num += 1
            formatted_string = "\n".join([f"{key}: {value}" for key, value in d.items()]) + f'\n\nالاجمالي:{St}'
            for i in l:
                try:
                    bot.send_message(str(i), str(formatted_string) + f'\n\n رقم الهاتف: {phoneNumber}')
                except Exception as e:
                    bot.send_message('1626922754', e)
                    continue
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)