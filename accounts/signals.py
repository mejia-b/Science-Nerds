from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Customer


def customer_profile(sender, instance, created, **kwargs):
    if created:
          group = Group.objects.get(name='customer')
          instance.groups.add(group)
          # Upon saving the info entered from the form in the above user variable
          # We are able to create a customer object and associate a user instance to the customer model object.
          # In order to populate other attributes in the customer model, we just type out the correct
          # keyword attribute name, ex. name=user.username etc. 
          Customer.objects.create(user=instance, name=instance.username, email=instance.email)
          print('Profile Created!')
          
post_save.connect(customer_profile, sender=User)