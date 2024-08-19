// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;
contract Policy1  {
    enum PolicyState {Active, Deactivated}

    mapping(address => bool) public authorities;

    // VARIABLES
    PolicyState policyState;
    uint startTime;
    uint endTime;
    uint presentTime;
    // EVENTS
    event AccessDenied( string message, uint presentTime, uint startTime, uint endTime);
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
    constructor(uint _startTime, uint _endTime){
        policyState = PolicyState.Active;
        authorities[msg.sender] = true;
        startTime = _startTime;
        endTime = _endTime;

    }    
    function setPolicyState(PolicyState _policyState) public authorities_only(){
        policyState = _policyState;
    }
    function getCurrentTime() internal view returns (uint256 ) {
        uint256 totalSeconds = block.timestamp % 86400; // Seconds in a day
        uint presentHours = totalSeconds / 3600 +6; 
        return presentHours ;
    }
    function checkPolicy()public onlyWhenActive returns (bool){
        presentTime = getCurrentTime();
        if(startTime <= presentTime && presentTime <= endTime){
            emit AccessApproved( "Time restriction passed!" );

            return true;
        }
        else{
            emit AccessDenied( "Time restriction!!", presentTime, startTime, endTime);
            return false;
        }
    }
}