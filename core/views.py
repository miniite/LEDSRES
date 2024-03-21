from django.shortcuts import render

# Create your views here.
# Calling Frontend
def root(request):
    return render(request,"base.html")
    