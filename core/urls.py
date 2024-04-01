from django.urls import path, include 
from .views import root, loginning, joinning, prof, trading, into_insight


urlpatterns = [
    path("",root),
    path('login/', loginning, name="login"),
    path('signup/', joinning, name="signup"),
    path('profile/', prof, name="profile"),
    path('trade/', trading, name="trade"),
    path('insight/', into_insight, name="insight")
]