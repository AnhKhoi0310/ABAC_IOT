from web3 import Web3
import json
import os
from dotenv import load_dotenv
load_dotenv()

def add_object():
    infura_url = f"https://sepolia.infura.io/v3/{os.getenv('WEB3_INFURA_PROJECT_ID')}"
    web3 = Web3(Web3.HTTPProvider(infura_url)) 

    with open('build/contracts/ObjectAttribute.json') as f:
        contract_json = json.load(f)
    
    abi = contract_json['abi']
    contract_address = os.getenv('ObjectAttribute') 

    contract = web3.eth.contract(address=contract_address, abi=abi)

    # value = contract.functions.getValue().call()
    # print(f"The stored value is: {value}")

    # get the account from private_key
    private_key = os.getenv("PRIVATE_KEY")
    account = web3.eth.account.from_key(private_key)
    # get gurrent nonce
    nonce = web3.eth.get_transaction_count(account.address)

    tx = contract.functions.add_object(
        os.getenv("ObjectAddress"), # put address
        "Camera1",
        60,
        0,
        0
        ).build_transaction({
        'from': account.address,
        'nonce':nonce,
        'gas': 2000000, # random 
        'gasPrice': web3.to_wei('50', 'gwei') # increase so that it is more attractive for miners
    })
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    try: 
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Transaction hash: {web3.to_hex(tx_hash)}")

        # Wait for the transaction receipt
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction receipt: {tx_receipt}")
    except ValueError as e:
        print(f"Error sending transaction: {e}")

add_object()