from brownie import Device, SubjectAttribute, ObjectAttribute, Policy1, Policy2, Policy3, Policy4, Policy5, Policy6, BasePolicy, accounts

def main():
    admin  = accounts[0]
    subject_lock = accounts[1]
    object_camera = accounts[2]
    base_policy_contract = BasePolicy[-1]
    output = base_policy_contract.access_control(
        subject_lock,
        object_camera,
        {"from": admin, "gas_limit": 1000000}
    )
    print("output",output['log'])