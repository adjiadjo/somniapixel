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

    latest_block = w3.eth.get_block('latest')
    base_fee = latest_block.get('baseFeePerGas', w3.to_wei(1, 'gwei'))

    # Auto-adjust priority fee
    suggested_priority_fee = w3.to_wei(2, 'gwei')  # base tip
    if base_fee > w3.to_wei(20, 'gwei'):
        suggested_priority_fee = w3.to_wei(3, 'gwei')
    if base_fee > w3.to_wei(50, 'gwei'):
        suggested_priority_fee = w3.to_wei(5, 'gwei')
    if base_fee > w3.to_wei(100, 'gwei'):
        suggested_priority_fee = w3.to_wei(8, 'gwei')

    max_fee_per_gas = base_fee + suggested_priority_fee + (base_fee // 5)  # +20% buffer

    txn = contract.functions.colorPixel(x, y, color).build_transaction({
        'from': account.address,
        'value': w3.to_wei(0.01, 'ether'),
        'gas': 300000,
        'maxFeePerGas': max_fee_per_gas,
        'maxPriorityFeePerGas': suggested_priority_fee,
        'nonce': nonce,
        'chainId': w3.eth.chain_id
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

    print(f"[{i+1}/{loop_count}] Transaction sent:")
    print(f"  Hash: {tx_hash.hex()}")
    print(f"  Pixel: (x={x}, y={y})")
    print(f"  Color: #{color:06X}")
    print(f"  baseFeePerGas: {w3.from_wei(base_fee, 'gwei')} gwei")
    print(f"  maxPriorityFeePerGas: {w3.from_wei(suggested_priority_fee, 'gwei')} gwei")
    print(f"  maxFeePerGas: {w3.from_wei(max_fee_per_gas, 'gwei')} gwei")
    print("-" * 50)

    time.sleep(3)

print("✅ Done!")
