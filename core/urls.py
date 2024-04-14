from django.urls import path, include 

from .views import root, CustomLoginView, registration, prof, trading, into_insight, logout_view


urlpatterns = [
    path("",root),
    path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', registration, name="signup"),
    path('profile/', prof, name="profile"),
    path('trade/', trading, name="trade"),
    path('insight/', into_insight, name="insight"),
    path('logout/', logout_view, name="logout")
]