from django import forms
from django.forms import ModelForm
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name','last_name','email', 'password1', 'password2']

class UserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = '__all__'
		# exclude = ['user']
