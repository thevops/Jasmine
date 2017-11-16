from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # authentication
from django.contrib.auth import authenticate, login, logout  # authentication
from .forms import LoginForm

def login_view(request):
    """ Get username, password and authenticate """
    if request.method == "POST":
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = loginform.cleaned_data['username']
            password = loginform.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('controller:start_view')
            else:
                messages.error(request, 'Invalid login or password !!!')
                return redirect('accounts:login_view')
    else:
        loginform = LoginForm()
        data = {
            "loginform": loginform
        }
        return render(request, 'accounts/login.html', data)

@login_required
def logout_view(request):
    """ Logout current user """
    logout(request)
    return redirect('controller:start_view')

