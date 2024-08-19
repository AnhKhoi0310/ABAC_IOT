from brownie import network, config, Device, SubjectAttribute, ObjectAttribute, Policy1, Policy2, Policy3, Policy4, Policy5, Policy6, BasePolicy, accounts
from dotenv import load_dotenv
import os

load_dotenv()
def main():
    private_key = os.getenv("PRIVATE_KEY")
    admin = accounts.add(private_key)

    # Ensure the Sepolia network is active
    if network.is_connected():
        print(f"Already connected to network '{network.show_active()}'")
    else:
        network.connect("sepolia")

    # Deploy the contract
    # device_contract= Device.deploy({"from": admin})
    # subject_attribute_contract = SubjectAttribute.deploy({"from": admin})
    # object_attribute_contract = ObjectAttribute.deploy({"from": admin})
    # policy1_contract = Policy1.deploy(8, 22,{"from": admin})
    # policy2_contract = Policy2.deploy(10,{"from": admin})
    # policy3_contract = Policy3.deploy({"from": admin})
    # policy4_contract = Policy4.deploy({"from": admin})
    # policy5_contract = Policy5.deploy({"from": admin})
    # policy6_contract = Policy6.deploy(1800,{"from": admin})
    BasePolicy_contract =  BasePolicy.deploy(
        "0x6a5E1F9480E7BE55CaD7a41a412866C22ff3FE90", #SubjectAttribute
        "0x03986844645D8Db19802dEddc69A690284FBA1dE", #ObjectAttribute
        "0x23b6DA8b86CaE904DB8085A61F140DAe95D4CaD0", #Policy1
        "0x82E31cE4c28cFA0b469012681dcC1d048C6222C5", #Policy2
        "0xd99b1A7368615B471EEcb4579Ff3525fFcF88Ad7", #Policy3
        "0x01E7124EDBFAA47F847098BF3546629775df46c1", #Policy4
        "0x44152d23a3A095b06AC07611B208A748E0C8152C", #Policy5
        "0x5E192f482886Cf6A5D4058A62b1379Dc8250ce04", #Policy6
        {"from": admin}
    )

    # print("Contract deployed at:", policy_contract.address)
