from django.shortcuts import render
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, CartSerializer, CartItemSerializer, CustomerSerializer
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Category, Product, Order, OrderItem, Cart, CartItem, Customer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.pagination import PageNumberPagination
# Import the Celery task for sending confirmation emails
from .tasks import send_order_confirmation_email



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly] # Allow all users to view categories, but only admins can create, update, or delete
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']



# Cache the list view for 15 minutes (900 seconds)
@method_decorator(cache_page(60 * 15), name='list')
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]  # Allow all users to view products, but only admins can create, update, or delete
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'category__name']
    ordering_fields = ['price']




class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username', 'status']

    def perform_create(self, serializer):
        # Save the order instance
        order = serializer.save(user=self.request.user)

        # Prepare email details
        user_email = order.user.email
        order_id = order.id
        delivery_type = getattr(order, 'delivery_type', 'delivery') 
        address = getattr(order, 'address', None)

        # Send the confirmation email in the background
        send_order_confirmation_email.delay(
            user_email=user_email,
            order_id=order_id,
            delivery_type=delivery_type,
            address=address
        )
        # The user will receive an email after checkout automatically


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['order__id', 'product__name']


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username']


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['cart__id', 'product__name']


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username', 'name', 'email']
    