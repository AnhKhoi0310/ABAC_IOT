// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;
contract Policy2  {
    enum PolicyState {Active, Deactivated}

    mapping(address => bool) public authorities;

    // VARIABLES
    PolicyState policyState;
    uint presentTime;
    uint restricted_interval;
    // EVENTS
    event AccessDenied( string message);
    event AccessApproved( string message);
    // MODIFIERS
    modifier authorities_only(){
        require(authorities[msg.sender] == true, "Sender is not an authority.");
        _;
    }
    modifier onlyWhenActive(){
        require(policyState == PolicyState.Active, "Policy2 is not Active");
        _;
    }
    //CONSTRUCTOR
    constructor( uint _restricted_interval){
        policyState = PolicyState.Active;
        restricted_interval = _restricted_interval;
        authorities[msg.sender] = true;

    }

    function setPolicyState(PolicyState _policyState) public authorities_only(){
        policyState = _policyState;
    }

    function checkPolicy(uint256  lastUpdated)public onlyWhenActive() returns (bool){
        presentTime = block.timestamp;
        if( presentTime - lastUpdated >=restricted_interval ){
            emit AccessApproved( "Time Interval restriction passed!");
            return true;
        }
        else{
            emit AccessDenied( "Time Interval restriction!!");
            return false;
        }
    }
}