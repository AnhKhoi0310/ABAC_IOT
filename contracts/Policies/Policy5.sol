// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;
import "contracts/SubjectAttribute.sol";
import "contracts/ObjectAttribute.sol";
contract Policy5{
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
        require(policyState == PolicyState.Active, "Policy5 is not Active");
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

    function checkPolicy(Device.Zone sub_zone , Device.Zone obj_zone ) public  onlyWhenActive() returns (bool){
        if(sub_zone == obj_zone ){ 
            emit AccessApproved("Subject and Object Zone approved!"); 
            return true;
        }
        else{
            emit AccessDenied( "Subject and Object not in the same Zone!");
            return false; 
        }
        }
}