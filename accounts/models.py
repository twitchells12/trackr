from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    email = models.EmailField(max_length=254,null=True)
    phone = models.CharField(max_length=15,null=True)
    address = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=50,null=True)
    state = models.CharField(max_length=50,null=True)
    zip = models.CharField(max_length=10,null=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    is_manager = models.BooleanField(default=False,null=True)
    def __str__(self):
        return self.user.username
