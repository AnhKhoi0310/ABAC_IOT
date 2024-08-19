// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;
import "contracts/SubjectAttribute.sol";
import "contracts/ObjectAttribute.sol";
contract Policy4{
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
        require(policyState == PolicyState.Active, "Policy4 is not Active");
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

function checkPolicy(Device.Category sub_category, uint sub_trust, uint obj_trust) public onlyWhenActive() returns (bool) {
    if (sub_category == Device.Category.Monitoring) { 
        if (sub_trust >= 80) {
            emit AccessApproved("Subject's trust approved!"); 
            return true;
        } else {
            emit AccessDenied("Subject's trust not approved!"); 
            return false;
        }
    }
    else if (sub_category == Device.Category.Security) {
        if (sub_trust >= 50 && obj_trust >= 50) {
            emit AccessApproved("Subject's & Object's trust approved!"); 
            return true;
        } else {
            emit AccessDenied("Subject's & Object's trust not approved!"); 
            return false;
        }
    }
    else if (sub_category == Device.Category.Health) {
        if (sub_trust >= 30 && obj_trust >= 30) {
            emit AccessApproved("Subject's & Object's trust approved!"); 
            return true;
        } else {
            emit AccessDenied("Subject's & Object's trust not approved!"); 
            return false;
        }
    }
    else if (sub_category == Device.Category.Entertainment) {
        if (sub_trust >= 10 && obj_trust >= 10) {
            emit AccessApproved("Subject's & Object's trust approved!"); 
            return true;
        } else {
            emit AccessDenied("Subject's & Object's trust not approved!"); 
            return false;
        }
    }
    else{
        emit AccessDenied("Subject's & Object's trust not approved!"); 
        return false;
    }
}

}