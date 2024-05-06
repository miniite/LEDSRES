from django.urls import path, include 

from .views import root, CustomLoginView, registration, prof, auctions, into_insight, logout_view, auctionCreate, place_bid, insights


urlpatterns = [
    path("",root),
    path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', registration, name="signup"),
    path('profile/', prof, name="profile"),
    path('trade/', auctions, name="trade"),
    path('create-auction/', auctionCreate, name="create-auction"),
    path('<auction_id>/bid', place_bid, name="place_bid"),
    path('insight/', into_insight, name="insight"),
    path('logout/', logout_view, name="logout"),
    path('insights/', insights, name="insights")
]