from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutPage,name='logout'),
    path('register/',views.registerPage,name='register'),
    path('profile/',views.profilePage,name='profile'),
    path('update/',views.profileUpdatePage,name='update'),

]
