
import json
from web3 import Web3


pk = "412d4b25435ce6d5a107a6e17d3bab167cc8518c319af92f5f79f291099fbf2d"

abi = [
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "startBid",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "endTime",
				"type": "uint256"
			}
		],
		"name": "AuctionCreated",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "id",
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
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_auctionId",
				"type": "uint256"
			}
		],
		"name": "bid",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "id",
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
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "id",
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
		"name": "BidRefunded",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_startBid",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_duration",
				"type": "uint256"
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
				"name": "_auctionId",
				"type": "uint256"
			}
		],
		"name": "finalizeAuction",
		"outputs": [],
		"stateMutability": "nonpayable",
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
		"name": "auctions",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"internalType": "address payable",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "startBid",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "highestBid",
				"type": "uint256"
			},
			{
				"internalType": "address payable",
				"name": "highestBidder",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "endTime",
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
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "bids",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

infura_url = "https://sepolia.infura.io/v3/c22cb83633ff42cbab662e654c1f7834"
web3 = Web3(Web3.HTTPProvider(infura_url))
print("Connected:", web3.is_connected())

contract_address = "0x69a7D6fa5A2FeD4E09FF20Aa0eb7dcB06adcbeb9"
contract_abi = abi
checksum_address = Web3.to_checksum_address(contract_address)


contract = web3.eth.contract(address=checksum_address, abi=contract_abi)
# print(contract.address)


def create_auction(start_bid, duration, pk):
    try:
        account = web3.eth.account.from_key(pk)  # Use your Ethereum account private key

        start_bid_wei = web3.to_wei(start_bid, 'ether')
        suggested_gas_price = web3.eth.gas_price
        increased_gas_price = int(suggested_gas_price * 1.1)  # Increase the gas price by 10%

        transaction = contract.functions.createAuction(start_bid_wei, duration).build_transaction({
            'chainId': 11155111,  # Make sure this is the correct chain ID
            'gas': 200000,
            'gasPrice': increased_gas_price,
            'nonce': web3.eth.get_transaction_count(account.address, 'pending'),
        })
        
        signed_txn = web3.eth.account.sign_transaction(transaction, account.key)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print("Transaction hash:", txn_hash.hex())

        receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
        for log in receipt.logs:
            event = contract.events.AuctionCreated().process_receipt(receipt)
            if event:
                    auction_id = event[0]['args']['id']
                    print("Auction ID:", auction_id)
                    return auction_id

    except Exception as e:
        print("An error occurred:", e)
        return None


def bt_place_bid(auction_id, bid_amount, pk):
    account = web3.eth.account.from_key(pk)
    bid_amount_wei = web3.to_wei(bid_amount, 'ether')
    transaction = contract.functions.bid(auction_id).build_transaction({
        'value': bid_amount_wei,
        'chainId': 11155111,
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': web3.eth.get_transaction_count(account.address),
    })
    signed_txn = web3.eth.account.sign_transaction(transaction, account.key)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("Transaction hash:", txn_hash.hex())
    receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
    return receipt

