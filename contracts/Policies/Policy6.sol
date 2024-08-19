// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;
contract Policy6  {
    enum PolicyState {Active, Deactivated}

    mapping(address => bool) public authorities;

    // VARIABLES
    PolicyState policyState;
    uint presentTime;
    uint restricted_age;
    // EVENTS
    event AccessDenied( string message);
    event AccessApproved( string message);
    // MODIFIERS
    modifier authorities_only(){
        require(authorities[msg.sender] == true, "Sender is not an authority.");
        _;
    }
    modifier onlyWhenActive(){
        require(policyState == PolicyState.Active, "Policy6 is not Active");
        _;
    }
    //CONSTRUCTOR
    constructor( uint _restricted_age){
        policyState = PolicyState.Active;
        restricted_age = _restricted_age; // in Seconds
        authorities[msg.sender] = true;

    }

    function setPolicyState(PolicyState _policyState) public authorities_only(){
        policyState = _policyState;
    }

    function checkPolicy(uint sub_age, uint obj_age)public onlyWhenActive() returns (bool){
        presentTime = block.timestamp;
        if( (presentTime - sub_age >= restricted_age )&& (presentTime - obj_age >= restricted_age)){
            emit AccessApproved( "Subject's & Object's age restriction passed!");
            return true;
        }
        else{
            emit AccessDenied( "Age restriction!!");
            return false;
        }
    }
}