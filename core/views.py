from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
# Calling Frontend
def root(request):
    return render(request,"index.html")

def loginning(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page
            return redirect('index.html')
        else:
            # Return an invalid login message
            messages.error(request, 'Invalid email or password. Please try again.')
    return render(request, 'login.html')


def joinning(request):
    return render(request,"signup.html")

def prof(request):
    return render(request,"profile.html")

def trading(request):
    return render(request,"trade.html")

def into_insight(request):
    return render(request,"insight.html")