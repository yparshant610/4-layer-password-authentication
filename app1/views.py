from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import UserDevice
from .forms import ContactForm
from django.http import JsonResponse
from django.utils import timezone
from django.http import HttpResponseForbidden

# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your Password and Confirm Password are not same")
        else:
            try:
                # Attempt to create a new user
                my_user = User.objects.create_user(uname, email, pass1)
                my_user.save()
                return redirect('login')
            except IntegrityError:
                # Handle the case where the username is not unique
                return HttpResponse("Username is already taken. Please choose a different username.")
    return render(request, 'signup.html')

def LoginPage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        form = ContactForm(request.POST) 
        pass1=request.POST.get('pass')
        user= authenticate(request, username=username, password=pass1)
        if user is not None and form.is_valid():
            login(request, user)
            # Check device limit
            if UserDevice.objects.filter(user=user).count() >= 3:
                logout(request)
                return HttpResponseForbidden("Device limit exceeded. Logout from other devices to login.")
            else:
                # Create or update device entry
                device_name = request.POST.get('device_name')
                UserDevice.objects.update_or_create(user=user, device_name=device_name, defaults={'last_login': timezone.now()})
                return redirect('home')   
        elif user is None :
            return HttpResponse("Username or password is incorrect")
        else: 
            return HttpResponse("OOPS! Bot suspected.") 
            
    else: 
        form = ContactForm()
        
    return render(request, 'login.html', {'form':form})
    

def LogoutPage(request):
    if request.user.is_authenticated:
        UserDevice.objects.filter(user=request.user, device_name=request.device_name).delete()
    logout(request)
    return redirect('login')



