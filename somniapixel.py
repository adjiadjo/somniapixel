from web3 import Web3
import random
import time
from getpass import getpass

# Connect to Somnia Shannon testnet RPC
w3 = Web3(Web3.HTTPProvider("https://dream-rpc.somnia.network"))

# Contract details
contract_address = '0x496eF0E9944ff8c83fa74FeB580f2FB581ecFfFd'
abi = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "x", "type": "uint256"},
            {"internalType": "uint256", "name": "y", "type": "uint256"},
            {"internalType": "uint24", "name": "color", "type": "uint24"}
        ],
        "name": "colorPixel",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]

contract = w3.eth.contract(address=contract_address, abi=abi)

# Get private key and loop count from user
private_key = getpass("Enter your wallet private key: ")
loop_count = int(input("How many pixels do you want to color? "))

account = w3.eth.account.from_key(private_key)

for i in range(loop_count):
    x = random.randint(0, 1023)
    y = random.randint(0, 1023)
    color = random.randint(0, 0xFFFFFF)  # Random RGB

    nonce = w3.eth.get_transaction_count(account.address)
    txn = contract.functions.colorPixel(x, y, color).build_transaction({
        'from': account.address,
        'value': w3.to_wei(0.01, 'ether'),
        'gas': 300000,
        'gasPrice': w3.to_wei('1', 'gwei'),
        'nonce': nonce,
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    
    # Use signed_txn['rawTransaction'] instead of signed_txn.rawTransaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Print the transaction hash
    print(f"Transaction Hash: {tx_hash.hex()}")

    print(f"[{i+1}/{loop_count}] Transaction sent:")
    print(f"  Hash: {tx_hash.hex()}")
    print(f"  Pixel: (x={x}, y={y})")
    print(f"  Color: #{color:06X}")
    print("-" * 50)

    time.sleep(3)

print("✅ Done!")
