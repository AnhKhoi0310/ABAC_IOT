# This file is for manually change Subject Attribute
from web3 import Web3
import json
import os
from dotenv import load_dotenv
load_dotenv()

def change_attribs(SubjectAddress =''):
    if SubjectAddress =='':
        SubjectAddress = os.getenv("SubjectAddress")
    infura_url = f"https://sepolia.infura.io/v3/{os.getenv('WEB3_INFURA_PROJECT_ID')}"
    web3 = Web3(Web3.HTTPProvider(infura_url)) 

    with open('../build/contracts/SubjectAttribute.json') as f:
        contract_json = json.load(f)
    
    abi = contract_json['abi']
    contract_address = os.getenv('SubjectAttribute') 

    contract = web3.eth.contract(address=contract_address, abi=abi)

    # get the account from private_key
    private_key = os.getenv("PRIVATE_KEY")
    account = web3.eth.account.from_key(private_key)
    # get gurrent nonce
    nonce = web3.eth.get_transaction_count(account.address)
    # Get current trust
    tx = contract.functions.change_attribs(
        os.getenv("SubjectAddress"),
        "",
        0,
        80,
        0,
        0,
        [],
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
        if tx_receipt.logs:
            print("\nLogs:")
            for log in tx_receipt.logs:
                # Decode log data
                for event_abi in abi:
                    if event_abi.get('type') == 'event':
                        event_signature = web3.keccak(text=f"{event_abi['name']}({','.join([input['type'] for input in event_abi['inputs']])})").hex()
                        if log['topics'][0].hex() == event_signature:
                            event_name = event_abi['name']
                            # Decode log data
                            event_data = contract.events[event_name]().process_log(log)
                            print(f"Event Name: {event_name}")
                            print(f"Data: {event_data.args}")
                            
                            if event_name == "SubjectChanged":
                                return True
                            break
                else:
                    print(f"Unknown event log")
    except ValueError as e:
        print(f"Error sending transaction: {e}")
    

change_attribs()