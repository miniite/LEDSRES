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

from .models import Auction, Bid
from web3 import Web3, HTTPProvider



web3 = Web3(Web3.HTTPProvider('https://eth-sepolia.g.alchemy.com/v2/FK4PztcimYW1P23ms-eb5wtGjNRFBbj0'))  # Update this URL


contract_address = '0x0796b731C0a3e2e00363D45Ee0b21FEe79509C9A'
contract_abi = [
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "auctionId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "endTime",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "address",
				"name": "beneficiary",
				"type": "address"
			}
		],
		"name": "AuctionCreated",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "auctionId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "address",
				"name": "winner",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "AuctionEnded",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "auctionId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "address",
				"name": "bidder",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "BidPlaced",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "duration",
				"type": "uint256"
			},
			{
				"internalType": "address payable",
				"name": "beneficiary",
				"type": "address"
			}
		],
		"name": "createAuction",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "auctionId",
				"type": "uint256"
			}
		],
		"name": "endAuction",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "auctionId",
				"type": "uint256"
			}
		],
		"name": "placeBid",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "auctionCount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "auctionData",
		"outputs": [
			{
				"internalType": "address payable",
				"name": "beneficiary",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "endTime",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "highestBidder",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "highestBid",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "ended",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

web3.eth.default_account = '0xcAa25d054cD09Df5D8d5Cd170094B5e55a1c745f'

contract = web3.eth.contract(address=contract_address, abi=contract_abi)


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
            return redirect(reverse('login'))  # Redirect to the login page after successful registration
        else:
            # If the form is not valid, rerender the signup page with the form to show errors
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# def joinning(request):
#     return render(request,"signup.html")

def prof(request):
    return render(request,"profile.html")

def into_insight(request):
    return render(request,"insight.html")


def logout_view(request):
    logout(request)
    return redirect('/') 



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
        beneficiary_address = user.eth_address

        breakpoint()
        tx_hash = contract.functions.createAuction(
            duration,
            str(beneficiary_address)
        ).transact({'from': web3.eth.default_account})  # Ensure the default_account is set correctly
        
        # Wait for transaction to be mined
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status:
            auction = Auction.objects.create(quantity=quantity, start_bid=start_bid, end_date=end_date, owner=user, contract_address=contract_address)
            messages.success(request, "Auction created successfully on the blockchain.")
        else:
            messages.error(request, "Failed to create auction on the blockchain.")
        

        auction = Auction.objects.create(quantity=quantity, start_bid=start_bid, end_date=end_date, owner=user)
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
        if bid_amount:
            tx_hash = contract.functions.bid(auction_id).transact({
                'from': web3.eth.default_account,  # Set to the current user's address
                'value': web3.to_wei(bid_amount, 'ether')
            })
            
            # Wait for transaction to be mined
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt.status:
                messages.success(request, "Bid placed successfully on the blockchain.")
            
                bid = Bid(user=request.user, auction=auction, amount=bid_amount)
                bid.save()
            messages.success(request, "Bid placed successfully.")
            return redirect('trade')
        else:
            messages.error(request, "Please enter a valid bid amount.")

    return render(request, 'auction-create.html', {'auction': auction, 'user':request.user})