from brownie import Device, SubjectAttribute, ObjectAttribute, Policy1, Policy2, Policy3, Policy4, Policy5, Policy6, BasePolicy, accounts

def main():
    admin  = accounts[0]
    obj_contract = ObjectAttribute[-1]
    output = obj_contract.add_object(
        accounts[2],
        "Camera1",
        5,
        0,
        0,
        {"from": admin}
        )
    # print(output)