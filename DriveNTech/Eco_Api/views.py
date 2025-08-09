from django.shortcuts import render
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, CartSerializer, CartItemSerializer, CustomerSerializer, WishlistSerializer, WishlistItemSerializer, ReviewSerializer, AddressSerializer, UserProfileSerializer, RegisterSerializer
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Category, Product, Order, OrderItem, Cart, CartItem, Customer, Wishlist, WishlistItem, Review, Address, Profile
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.pagination import PageNumberPagination
# Import the Celery task for sending confirmation emails
from .tasks import send_order_confirmation_email
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User




class RegisterViewSet(viewsets.ViewSet):
    """
    this viewset handles user registration
    """
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Create the user and profile
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email']
            )
            Profile.objects.create(user=user)
            return Response({'detail': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    
    def get_object(self):
        return self.request.user.profile



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
    # Only return orders belonging to the current user
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
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
         # The user will receive an email after checkout automatically
        send_order_confirmation_email.delay(
            user_email=user_email,
            order_id=order_id,
            delivery_type=delivery_type,
            address=address
        )
       
    # Custom action to update order status
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated]) # this decorator allows us to add custom actions to the viewset
    def update_status(self, request, pk=None): 
        order = self.get_object()
        # Check if the user is an admin
        if not request.user.is_staff:
            return Response({'detail': 'Only admin can update order status.'}, status=status.HTTP_403_FORBIDDEN)
        # Get the new status from the request data
        new_status = request.data.get('status')
        # Validate the new status
        if new_status not in dict(order.STATUS_CHOICES):
            return Response({'detail': 'Invalid status value.'}, status=status.HTTP_400_BAD_REQUEST)
        # Update the order status and save it
        order.status = new_status
        order.save()
        # Send an email notification to the user about the status update, it will call the celery task
        send_order_status_update_email.delay(
            user_email=order.user.email,
            order_id=order.id,
            new_status=new_status
        )
        # Return a success response
        # This response will be sent to the user after the order status is updated
        return Response({'detail': f'Order status updated to {new_status}.'}, status=status.HTTP_200_OK)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['order__id', 'product__name']


class CartViewSet(viewsets.ModelViewSet):
    # Only return carts belonging to the current user
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
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


class WishlistViewSet(viewsets.ModelViewSet):
    # Only return wishlists belonging to the current user
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username']


class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['wishlist__id', 'product__name']


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['product__name', 'user__username']


class AddressViewSet(viewsets.ModelViewSet):
    # Only return addresses belonging to the current user
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username', 'city', 'state', 'country']


class RegisterViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for user registration.
    """
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Create the user and profile
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email']
            )
            Profile.objects.create(user=user)
            return Response({'detail': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    