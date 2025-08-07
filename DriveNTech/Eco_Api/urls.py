from django.urls import path
from .views import CategoryViewSet, ProductViewSet, OrderViewSet, OrderItemViewSet, CartViewSet, CartItemViewSet, CustomerViewSet, WishlistViewSet, WishlistItemViewSet, ReviewViewSet, AddressViewSet
from Eco_Api.swagger import schema_view

urlpatterns = [
    path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
    path('categories/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='category-detail'),

    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list'),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='product-detail'),

    path('orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='order-list'),
    path('orders/<int:pk>/', OrderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='order-detail'),

    path('order-items/', OrderItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='orderitem-list'),
    path('order-items/<int:pk>/', OrderItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='orderitem-detail'),

    path('carts/', CartViewSet.as_view({'get': 'list', 'post': 'create'}), name='cart-list'),
    path('carts/<int:pk>/', CartViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='cart-detail'),

    path('cart-items/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='cartitem-list'),
    path('cart-items/<int:pk>/', CartItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='cartitem-detail'),

    path('customers/', CustomerViewSet.as_view({'get': 'list', 'post': 'create'}), name='customer-list'),
    path('customers/<int:pk>/', CustomerViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='customer-detail'),

    path('wishlists/', WishlistViewSet.as_view({'get': 'list', 'post': 'create'}), name='wishlist-list'),
    path('wishlists/<int:pk>/', WishlistViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='wishlist-detail'),

    path('wishlist-items/', WishlistItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='wishlistitem-list'),
    path('wishlist-items/<int:pk>/', WishlistItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='wishlistitem-detail'),

    path('reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='review-list'),
    path('reviews/<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='review-detail'),

    path('addresses/', AddressViewSet.as_view({'get': 'list', 'post': 'create'}), name='address-list'),
    path('addresses/<int:pk>/', AddressViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='address-detail'),

    # Swagger documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

