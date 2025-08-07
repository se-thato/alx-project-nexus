from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

#this code is used to create and save a user profile automatically when a new user is created
#it ensures that every user has a corresponding profile in the UserProfile model
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print(f"UserProfile created for user: {instance.username}")

#this code is used to save the user profile whenever the user instance is saved
#it ensures that any changes made to the user profile are saved to the database
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
    print(f"UserProfile saved for user: {instance.username}")
