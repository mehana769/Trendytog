
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from cart.models import Order
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration successful! you can now login.')
           # login(request,user)
            return redirect('accounts:login')
        
           
    else: 
        form=RegistrationForm()
    return render(request,'register.html',{'form':form})
    


def profile(request):
    user=request.user
    orders=Order.objects.filter(user=user)
    return render(request,'profile.html',{'user':user,'order':orders})

def logout_view(request):
    logout(request)
    return redirect('home:allprodcat')


from django.shortcuts import render

def profile_view(request):
    return render(request, 'profile.html')
