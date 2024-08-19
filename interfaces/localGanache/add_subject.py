from brownie import Device, SubjectAttribute, ObjectAttribute, Policy1, Policy2, Policy3, Policy4, Policy5, Policy6, BasePolicy, accounts

def main():
    admin  = accounts[0]
    sub_contract = SubjectAttribute[-1]
    output = sub_contract.addAuthority(
        accounts[1],
        "Lock1",
        5,
        0,
        0,
        {"from": admin}
        )
    # print(output)