from web3 import Web3

def create_new_address():
    # Create a new Web3 instance
    web3 = Web3()

    # Generate a new Ethereum account
    account = web3.eth.account.create()

    return account.address, account._private_key.hex()

# Generate and store the address and private key for the subject
subject_address, subject_private_key = create_new_address()

# Store or use the address and private key as needed
print(f"Account Address: {subject_address}")
print(f"Account Private Key: {subject_private_key}")