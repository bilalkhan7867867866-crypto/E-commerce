from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

def home(request):
    return render(request,'home.html')

def register(request):    
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        
    else:
        form = RegisterForm()

    context = {
        'form': form
    }

    return render(
        request,
        'accounts/register.html',
        context
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    else:
        form = AuthenticationForm()

    context = {
        'form': form
    }

    return render(
        request,
        'accounts/login.html',
        context
    )


def logout_view(request):
    """
    User Logout
    """

    logout(request)

    return redirect('login')