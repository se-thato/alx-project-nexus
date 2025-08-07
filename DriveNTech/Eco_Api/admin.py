from django.contrib import admin
from .models import Product, Category, Order, OrderItem, CartItem, Cart, Customer, Wishlist, WishlistItem, Review, Address


admin.site.register(Product)

admin.site.register(Category)

admin.site.register(Wishlist)

admin.site.register(WishlistItem)

admin.site.register(Review)

admin.site.register(Cart)

admin.site.register(CartItem)

admin.site.register(Order)

admin.site.register(OrderItem)

admin.site.register(Customer)

admin.site.register(Address)