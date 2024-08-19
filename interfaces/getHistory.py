from web3 import Web3
import json
import os
from dotenv import load_dotenv
load_dotenv()
def get_history(SubjectAddress):
    infura_url = f"https://sepolia.infura.io/v3/{os.getenv('WEB3_INFURA_PROJECT_ID')}"
    web3 = Web3(Web3.HTTPProvider(infura_url)) 
    with open('build/contracts/SubjectAttribute.json') as f:
        contract_json = json.load(f)
    
    abi = contract_json['abi']
    contract_address = os.getenv('SubjectAttribute') 

    contract = web3.eth.contract(address=contract_address, abi=abi)
    try:
        history = contract.functions.get_history(
            SubjectAddress,
        ).call()
        return history         
    except ValueError as e:
        print(f"Error sending transaction: {e}")
