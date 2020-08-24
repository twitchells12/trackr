from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import UserProfile

def user_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(
            user = instance,
            first_name = instance.first_name,
            last_name = instance.last_name,
            email = instance.email,
        )
        print('User created')
post_save.connect(user_profile,sender=User)
