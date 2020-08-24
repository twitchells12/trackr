from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, UserProfileForm
from .models import UserProfile
from django.contrib import messages
from teams.models import Team,TeamMember
# Create your views here.

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request,'Account Created for '+ username)

            return redirect('login')

    context = {'form':form}
    return render(request,'accounts/register.html',context)


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username OR password is incorrect')

    context = {}
    return render(request,'accounts/login.html',context)


def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profilePage(request):
    user = request.user.userprofile
    profile = UserProfileForm(instance=user)
    teamlist = list(Team.objects.filter(members=request.user))

    context = {'profile':profile,'teamlist':teamlist}
    return render(request,'accounts/profile.html',context)

@login_required(login_url='login')
def profileUpdatePage(request):
    user = request.user.userprofile
    form = UserProfileForm(instance=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile/')
    context = {'form':form}
    return render(request,'accounts/profileupdate.html',context)
