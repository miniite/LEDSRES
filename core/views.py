from datetime import timedelta
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.urls import reverse
from .forms import SignUpForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings

import os


import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from tensorflow.keras.initializers import Orthogonal





from .models import Auction, Bid
from web3 import Web3, HTTPProvider
from .utils import create_auction, bt_place_bid
from .predict import predict_future_values


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
            return redirect('/')
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
                messages.success(request, 'Your account has been created successfully! You can now log in.')
                return redirect(reverse('login'))  # Redirect to the login page after successful registration
            else:
                # If the form is not valid, rerender the signup page with the form to show errors
                return render(request, 'signup.html', {'form': form})
        else:
            form = SignUpForm()
            
        print(form.fields['region'].choices)     
        return render(request, 'signup.html', {'form': form})



# def joinning(request):
#     return render(request,"signup.html")

@login_required
def prof(request):
    return render(request,"profile.html")

@login_required
def into_insight(request):
    return render(request,"insight.html")


def logout_view(request):
    logout(request)
    return redirect('/') 


@login_required
def auctions(request):
    current_time = timezone.now()
    auctions = Auction.objects.filter(end_date__gte=current_time).order_by('end_date')
    context = {'auctions': auctions}
    return render(request, 'trade.html', context)

from django.shortcuts import render, redirect
from .models import Auction

def auctionCreate(request):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        start_bid = request.POST.get('bid')
        # Assuming 'end_date' is 12 AM the next day
        end_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        user = request.user
        duration = int((end_date - timezone.now()).total_seconds()) 
        beneficiary_address = user.private_address
        auction_id = create_auction(start_bid, duration, beneficiary_address)

        if auction_id:
            auction = Auction.objects.create(quantity=quantity, start_bid=start_bid, end_date=end_date, owner=user, contract_id=auction_id)
            messages.success(request, "Auction created successfully on the blockchain.")
        else:
            messages.error(request, "Failed to create auction on the blockchain.")

        return redirect('trade')  # Redirect to the list of auctions
    return render(request, 'auction-create.html')


def place_bid(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    current_time = timezone.now()
    # Check if auction has ended
    if current_time > auction.end_date:
        messages.error(request, "Auction has ended.")
        return redirect('trade')

    # Check if user has already placed a bid
    if Bid.objects.filter(user=request.user, auction=auction).exists():
        messages.error(request, "You have already placed a bid.")
        return redirect('trade')

    # Check if it's before 12 AM
    # if current_time.hour >= 0 and current_time.hour < 12:
    #     messages.error(request, "Bidding is not allowed after 12 AM.")
    #     return redirect('trade')

    if request.method == 'POST':
        bid_amount = request.POST.get('bid_amount')
        pk = request.user.private_address
        if bid_amount:
            acution_id = auction.contract_id
            breakpoint()
            receipt = bt_place_bid(auction_id, int(bid_amount), pk)
            if receipt.status:
                messages.success(request, "Bid placed successfully on the blockchain.")
            
                bid = Bid(user=request.user, auction=auction, amount=bid_amount)
                bid.save()
            messages.success(request, "Bid placed successfully.")
            return redirect('trade')
        else:
            messages.error(request, "Please enter a valid bid amount.")

    return render(request, 'auction-create.html', {'auction': auction, 'user':request.user})



from django.core.files.storage import FileSystemStorage
import pandas as pd
from joblib import load


import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from joblib import load
import numpy as np


def insights(request):
    if request.method == 'POST' and 'file' in request.FILES:
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        try:
            with fs.open(filename, 'rb') as file:
                df = pd.read_excel(file)
                df['Date'] = pd.to_datetime(df['Date'])
                df.set_index('Date', inplace=True)

                # Apply the same feature engineering as during training
                apply_feature_engineering(df)  # Ensure this function aligns with training

                # Check if feature count is correct
                expected_feature_count = 29  # Replace with the number of features your scaler expects
                feature_columns = [col for col in df.columns if col != 'Generation']
                if len(feature_columns) != expected_feature_count:
                    raise ValueError(f"Expected {expected_feature_count} features, but got {len(feature_columns)}")

                best_model_path = os.path.join(settings.BASE_DIR, "static", "model", "best_model.h5")
                best_model = load_model(best_model_path)

                # Load pre-fitted scalers
                scaler_feature = load(os.path.join(settings.BASE_DIR, "static", "model", "scaler_feature.joblib"))
                scaler_target = load(os.path.join(settings.BASE_DIR, "static", "model", "scaler_target.joblib"))

                # Prepare data for prediction
                last_known_features = scaler_feature.transform(df[feature_columns].iloc[-3:].values)

                N = 3
                future_steps = 7
                max_actual_value = df['Generation'].max()

                future_power_generation = predict_future_values(
                    best_model, last_known_features, scaler_feature, scaler_target, N, future_steps, max_actual_value)

                last_date = df.index[-1]
                future_dates = pd.date_range(start=last_date, periods=future_steps + 1, freq='D')[1:]

                plt.figure(figsize=(15, 7))
                plt.plot(future_dates, future_power_generation, 'r--', label='Predicted Future Power Generation')
                plt.gca().xaxis.set_major_locator(mdates.DayLocator())
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                plt.gcf().autofmt_xdate()
                plt.ylim(0, max(future_power_generation))
                plt.title('Predicted Future Power Generation')
                plt.xlabel('Date')
                plt.ylabel('Power Generation')
                plt.legend()

                plot_path = os.path.join(settings.MEDIA_ROOT, 'future_power_generation.png')
                plt.savefig(plot_path)
                plt.close()

                context = {'plot_url': settings.MEDIA_URL + 'future_power_generation.png'}
                return render(request, 'graph.html', context)
        except Exception as e:
            print(e)
            return render(request, 'trade.html', {'error': str(e)})

    return render(request, "insight.html")

def apply_feature_engineering(df):
    # Implement the exact same transformations here as you did when training the model
    # For example:
    df['rolling_mean'] = df['Generation'].rolling(window=3).mean()
    df['rolling_std'] = df['Generation'].rolling(window=3).std()
    df.dropna(inplace=True)
    return df


def predict_future_values(model, last_known_features, scaler_feature, scaler_target, N, future_steps, max_actual_value):
    future_predictions = []
    current_features = last_known_features.copy()

    for _ in range(future_steps):
        current_features_scaled = scaler_feature.transform(current_features[-N:])
        current_features_scaled = current_features_scaled.reshape(1, N, -1)
        
        # Predict the next value
        next_prediction_scaled = model.predict(current_features_scaled)
        next_prediction = scaler_target.inverse_transform(next_prediction_scaled).ravel()[0]
        
        # Ensure prediction is non-negative and does not exceed slightly above the maximum actual value
        next_prediction = max(0, min(next_prediction, max_actual_value * 1.05))
        
        # Append the prediction to the list
        future_predictions.append(next_prediction)
        
        # Add the next prediction to the current_features
        next_feature = np.zeros((1, current_features.shape[1]))
        next_feature[:, -1] = next_prediction  # Assuming last feature is the predicted feature
        current_features = np.vstack([current_features, next_feature])
    
    return future_predictions
