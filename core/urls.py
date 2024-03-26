from django.urls import path, include 
from .views import root,prof, trading, into_insight


urlpatterns = [
    path("",root),
    path('profile/', prof, name="profile"),
    path('trade/', trading, name="trade"),
    path('insight/', into_insight, name="insight")
]