from web3 import Web3
import json
import os
from dotenv import load_dotenv
load_dotenv()

def add_subject():
    infura_url = f"https://sepolia.infura.io/v3/{os.getenv('WEB3_INFURA_PROJECT_ID')}"
    web3 = Web3(Web3.HTTPProvider(infura_url)) 

    with open('build/contracts/SubjectAttribute.json') as f:
        contract_json = json.load(f)
    
    abi = contract_json['abi']
    contract_address = os.getenv('SubjectAttribute') 

    contract = web3.eth.contract(address=contract_address, abi=abi)

    # value = contract.functions.getValue().call()
    # print(f"The stored value is: {value}")

    # get the account from private_key
    private_key = os.getenv("PRIVATE_KEY")
    account = web3.eth.account.from_key(private_key)
    # get gurrent nonce
    nonce = web3.eth.get_transaction_count(account.address)

    tx = contract.functions.add_subject(
        os.getenv("Subject2Address"), # put address
        "Lock2",
        10,
        0,
        1
        ).build_transaction({
        'from': account.address,
        'nonce':nonce,
        'gas': 2000000, # random 
        'gasPrice': web3.to_wei('50', 'gwei') # increase so that it  more attractive for miners
    })
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    try: 
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Transaction hash: {web3.to_hex(tx_hash)}")

        # Wait for the transaction receipt
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        # print(f"Transaction receipt: {tx_receipt}")

        logs = tx_receipt['logs']
        for log in logs:
            try:
                # Process log to get event details
                event = contract.events.__dict__.get(log['topics'][0].hex())
                if event:
                    decoded_event = event.processLog(log)
                    print(f"Event: {decoded_event.event}")
                    print(f"Args: {decoded_event.args}")
                else:
                    print(f"Event not found for log: {log}")
            except Exception as e:
                print(f"Could not decode log: {log}")
                print(f"Error: {e}")
    
    except ValueError as e:
        print(f"Error sending transaction: {e}")

add_subject()