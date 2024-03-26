from django.shortcuts import render

# Create your views here.
# Calling Frontend
def root(request):
    return render(request,"index.html")
    
def prof(request):
    return render(request,"profile.html")

def trading(request):
    return render(request,"trade.html")

def into_insight(request):
    return render(request,"insight.html")