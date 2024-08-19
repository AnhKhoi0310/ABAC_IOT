from web3 import Web3
import json
import os
from eth_utils import to_checksum_address 
from dotenv import load_dotenv
load_dotenv()

def access_control(SubjectAddress ='', ObjectAddress = ''):
    infura_url = f"https://sepolia.infura.io/v3/{os.getenv('WEB3_INFURA_PROJECT_ID')}"
    web3 = Web3(Web3.HTTPProvider(infura_url)) 
    try:
        subject_checksum = to_checksum_address(SubjectAddress) # Only check for address format
        object_checksum = to_checksum_address(ObjectAddress)
    except Exception as e:
        print(f"Invalid address error: {e}")
        return False

    with open('build/contracts/BasePolicy.json') as f:
        contract_json = json.load(f)
    
    abi = contract_json['abi']
    contract_address = os.getenv('BasePolicy') 

    contract = web3.eth.contract(address=contract_address, abi=abi)
    # Check if subject if register
    # with open('build/contracts/SubjectAttribute.json') as f:
    #     subject_contract_json = json.load(f)
    
    # subject_abi = subject_contract_json['abi']
    # subject_contract_address = os.getenv('BasePolicy') 

    # subject_contract = web3.eth.contract(address=subject_contract_address, abi=subject_abi)
    # check_bitmap = subject_contract.functions.check_bitmap(
    #         SubjectAddress,
    #     ).call()
    # if(check_bitmap == False) :
    #     print("Subject not registered")
    #     return False

    # get the account from private_key
    private_key = os.getenv("PRIVATE_KEY")
    account = web3.eth.account.from_key(private_key)
    # get gurrent nonce
    nonce = web3.eth.get_transaction_count(account.address)

    tx = contract.functions.access_control(
        SubjectAddress,
        ObjectAddress
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
                            if event_name == "AccessGranted":
                                return True
                            break
                else:
                    print(f"Unknown event log")
                
                print(f"Data: {log['data']}")
                print(f"Topics: {log['topics']}")            
    except ValueError as e:
        print(f"Error sending transaction: {e}")

# access_control()