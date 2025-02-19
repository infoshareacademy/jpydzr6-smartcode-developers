from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def signup(request):
    return render(request,'users/signup.html')

#     if request.method == 'POST':
#
def login(request):
    return render(request, 'users/login.html')

def dashboard(request):
    return render(request, 'users/dashboard.html')




