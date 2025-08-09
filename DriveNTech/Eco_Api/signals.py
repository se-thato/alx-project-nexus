# signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from .models import Order, OrderItem, Product
from django.core.mail import send_mail
from django.db.models.signals import post_delete

#this signal creates a Profile instance whenever a User is created
#This ensures that every user has a profile associated with them
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


# This signal sends order confirmation email when Order is created
@receiver(post_save, sender=Order)
def send_order_confirmation_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject=f"Order #{instance.id} Confirmation",
            message=f"Hey thank you for your purchase, {instance.customer.user.username}!",
            from_email="thatoselepe53@gmail.com",
            recipient_list=[instance.customer.user.email],
            fail_silently=True,
        )

# this signal reduces the stock of a product when an OrderItem is created
# it ensures that the stock is updated accordingly
@receiver(post_save, sender=OrderItem)
def reduce_stock_on_order(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.stock -= instance.quantity
        product.save()


# this signal restores the stock of a product when an OrderItem is deleted
@receiver(post_delete, sender=OrderItem)
def restore_stock_on_order_delete(sender, instance, **kwargs):
    product = instance.product
    product.stock += instance.quantity
    product.save()

# This signal alerts when stock is low for a product
# it checks if the stock is below a certain threshold
@receiver(pre_save, sender=Product)
def alert_low_stock(sender, instance, **kwargs):
    if instance.stock <= 5:
        print(f"Stock is low for {instance.name}. Current stock: {instance.stock}")
        