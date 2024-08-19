// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;
import "contracts/SubjectAttribute.sol";
import "contracts/ObjectAttribute.sol";
import "contracts/Policies/Policy1.sol";
import "contracts/Policies/Policy2.sol";
import "contracts/Policies/Policy3.sol";
import "contracts/Policies/Policy4.sol";
import "contracts/Policies/Policy5.sol";
import "contracts/Policies/Policy6.sol";
contract BasePolicy{
    
    struct Subject {
        Device.State state;
        string name; // type od the device
        uint age; // Number of days since the device was first registered
        uint trust; // 1 to 10
        Device.Category category; 
        Device.Zone zone; // Location
        uint256 lastUpdated; //lastime send request
    }
    struct Object {
        Device.State state;
        string name; // type od the device
        uint age; // Number of days since the device was first registered
        uint trust; // 1 to 10
        Device.Category category; 
        Device.Zone zone; // Location
    }    
    // VARIABLES
    // These are contract addresses:
    address public subject_contract_address;
    address public object_contract_address;
    address public policy1_address;
    address public policy2_address;
    address public policy3_address;
    address public policy4_address;
    address public policy5_address;
    address public policy6_address;
    mapping(address => bool) public authorities;
    // EVENTS
    event AccessGranted(address indexed sub_addr, address indexed obj_addr);
    event AccessDenied(address indexed sub_addr, address indexed obj_addr, string message);
    event AuthenticationSuccess(address indexed sub_addr);
    event AuthenticationFailure(address indexed sub_addr);
    // MODIFIER
    modifier authorities_only(){
        require(authorities[msg.sender] == true, "Sender is not an authority.");
        _;
    }    
    constructor(address sub_con, address obj_con, address pol1_con, address pol2_con, 
    address pol3_con,address pol4_con, address pol5_con, address pol6_con) {
        authorities[msg.sender] = true;
        subject_contract_address = sub_con;
        object_contract_address = obj_con;
        policy1_address = pol1_con;
        policy2_address = pol2_con;
        policy3_address = pol3_con;
        policy4_address = pol4_con;
        policy5_address = pol5_con;
        policy6_address = pol6_con;
    }  

    //Add Authority
    function addAuthority(address authority) public authorities_only() {
        authorities[authority] = true;
    }

    //Remove Authority
    function removeAuthority(address authority) public authorities_only() {
        authorities[authority] = false;
    }

    function access_control(address sub_addr, address obj_addr) public returns (bool)  {
        SubjectAttribute subject_contract = SubjectAttribute(subject_contract_address);
        ObjectAttribute object_contract = ObjectAttribute(object_contract_address);
        // check if the subject (lock) is registered
        if(!subject_contract.check_bitmap(sub_addr)) {
            emit AccessDenied(sub_addr, obj_addr, "Subject not found.");
            emit AuthenticationFailure(sub_addr);
            return false;
        } else {
            emit AuthenticationSuccess(sub_addr);
        }
        // check if the object (camera) is registered
        if(!object_contract.check_bitmap(obj_addr)) {
            emit AccessDenied(sub_addr, obj_addr, "Object not found.");
            emit AuthenticationFailure(obj_addr);
            return false;
        } else {
            emit AuthenticationSuccess(obj_addr);
        }

        // Get subject info
        Subject memory sub_info;
        (sub_info.state, sub_info.name, sub_info.age, sub_info.trust,sub_info.category, sub_info.zone, sub_info.lastUpdated) 
        = subject_contract.subjects(sub_addr);
        // Get subject info
        Object memory obj_info;
        (obj_info.state, obj_info.name, obj_info.age, obj_info.trust,obj_info.category, obj_info.zone) 
        = object_contract.objects(obj_addr);
        // Check subject & object active status
        if(sub_info.state != Device.State.Active) {
            emit AccessDenied(sub_addr, obj_addr, "Subject is not active.");
            emit AuthenticationFailure(sub_addr);
            return false;
        
        } else if(obj_info.state != Device.State.Active) {
            emit AccessDenied(sub_addr, obj_addr, "Object is not active.");
            emit AuthenticationFailure(obj_addr);
            return false;
        }
        // Get contract info
        Policy1 policy1_contract = Policy1(policy1_address);
        Policy2 policy2_contract = Policy2(policy2_address);
        Policy3 policy3_contract = Policy3(policy3_address);
        Policy4 policy4_contract = Policy4(policy4_address);
        Policy5 policy5_contract = Policy5(policy5_address);
        Policy6 policy6_contract = Policy6(policy6_address);
        // Check policies
        if (policy1_contract.checkPolicy()== false){
            return false;
        }
        if( policy2_contract.checkPolicy(sub_info.lastUpdated) == false){
            return false;
        }
        // Change the "last updated" Attribute in Subject 
        uint256 current_time = block.timestamp;
        subject_contract.change_attribs(sub_addr,"" , 0, 0, Device.Category.Security, Device.Zone.Zone1, new uint256[](0) , current_time);
        // Push new request time to history
        subject_contract.push_history(sub_addr, current_time);
        
        if( policy3_contract.checkPolicy(sub_info.category, obj_info.category)== false){
            return false;
        }
        if( policy4_contract.checkPolicy(sub_info.category, sub_info.trust, obj_info.trust )== false){
            return false;
        }    
        if( policy5_contract.checkPolicy(sub_info.zone, obj_info.zone)== false) {
            return false;
        }     
        if( policy6_contract.checkPolicy(sub_info.age, obj_info.age)== false) {
            return false;
        }  
        emit AccessGranted(sub_addr, obj_addr);
        return true;
    }

}