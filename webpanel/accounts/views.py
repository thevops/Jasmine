from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # authentication
from django.contrib.auth import authenticate, login, logout  # authentication

def login_view(request):
    """ Get username, password and authenticate """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('controller:start_view')
        else:
            messages.error(request, 'Invalid login or password !!!')
            return render(request, 'accounts/login.html')
    else:
        return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    """ Logout current user """
    logout(request)
    return redirect('controller:start_view')

