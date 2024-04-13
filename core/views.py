from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.urls import reverse
from .forms import SignUpForm


# Create your views here.
# Calling Frontend
def root(request):
    return render(request,"index.html")


# def loginning(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)
#             # Redirect to a success page
#             return redirect('index.html')
#         else:
#             # Return an invalid login message
#             messages.error(request, 'Invalid email or password. Please try again.')
#     return render(request, 'login.html')


class CustomLoginView(View):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
             # Redirect to a success page
            return redirect('index.html')
        else:
            message = "Invalid email or password. Please try again."
            messages.error(request, message)  # Display error message

        return render(request, self.template_name, {'message': message})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
@login_required
def CustomLogout(request):
    logout(request)
    return HttpResponse("Loggged out")


def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))  # Redirect to login page after successful registration
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# def joinning(request):
#     return render(request,"signup.html")

def prof(request):
    return render(request,"profile.html")

def trading(request):
    return render(request,"trade.html")

def into_insight(request):
    return render(request,"insight.html")