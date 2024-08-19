// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;
import "contracts/SubjectAttribute.sol";
import "contracts/ObjectAttribute.sol";
contract Policy3{
    enum PolicyState {Active, Deactivated}

    mapping(address => bool) public authorities;
    // VARIABLES
    PolicyState policyState;
     //EVENTS
    event AccessDenied( string message);
    event AccessApproved( string message);
    // MODIFIERS
    modifier authorities_only(){
        require(authorities[msg.sender] == true, "Sender is not an authority.");
        _;
    }
    modifier onlyWhenActive(){
        require(policyState == PolicyState.Active, "Policy3 is not Active");
        _;
    }
    // CONSTRUCTOR
    constructor(){
        policyState = PolicyState.Active;
        authorities[msg.sender] = true;
    }

    function setPolicyState(PolicyState _policyState) public authorities_only(){
        policyState = _policyState;
    }

    function checkPolicy(Device.Category sub_category , Device.Category obj_category ) public  onlyWhenActive() returns (bool){
        if(sub_category == Device.Category.Monitoring){
            emit AccessApproved("Subject is a Monitor !"); 
            return true;
        }
        else if(sub_category == obj_category ){ 
            emit AccessApproved("Subject and Object Category match!"); 
        return true;
        }
        else{
            emit AccessDenied( "Subject and Object Category mismatch!");
            return false; 
        }
        }
}