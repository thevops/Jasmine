from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def start_view(request):
    return render(request, 'controller/index.html',)

@login_required
def add_host_view(request):
    return render(request, 'controller/add_host.html', )