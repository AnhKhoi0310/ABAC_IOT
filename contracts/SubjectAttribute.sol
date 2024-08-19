// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;
import "contracts/Device.sol";
contract SubjectAttribute {

    struct Subject {
        Device.State state;
        string name; // type of the device
        uint age; // Number of days since the device was first registered
        uint trust; // 1 to 10
        Device.Category category; 
        Device.Zone zone; // Location
        uint[] history;
        uint256 lastUpdated; //lastime send request
    }
    struct BloomFilter{
        uint256 bitmap;
        uint8 hash_count;
    }
    
    // VARIABLES
    mapping(address => bool) public authorities;
    uint256 num_subjects;
    BloomFilter filter;
    mapping (address => Subject) public subjects;
    constructor() {
        authorities[msg.sender] = true;
        num_subjects = 0;
        filter.bitmap = 0;
        filter.hash_count = 5;
    }

    event NewSubjectAdded(address sub_addr, string sub);
    event SubjectChanged(address sub_addr);
        // Modifier
    //Authorities Only
    modifier authorities_only(){
        require(authorities[msg.sender] == true, "Sender is not an authority.");
        _;
    }

    modifier sub_active(address sub_addr){
        require(subjects[sub_addr].state == Device.State.Active, "Object state is not active!");
        _;
    }

    function addAuthority(address authority) public authorities_only() {
        authorities[authority] = true;
    }
    function add_subject (
        address sub_addr,         
        string memory name, // type of the device
        uint trust, // 1 to 100
        Device.Category category, 
        Device.Zone zone // Location
        ) public authorities_only() {

        num_subjects++;
        subjects[sub_addr].state = Device.State.Active;
        //Subject Attributes:
        subjects[sub_addr].name = name;
        subjects[sub_addr].age = block.timestamp;
        subjects[sub_addr].trust = trust;
        subjects[sub_addr].category = category;
        subjects[sub_addr].zone = zone;
        subjects[sub_addr].history = new uint[](0);
        subjects[sub_addr].lastUpdated = block.timestamp;

        add_bitmap(sub_addr);

        emit NewSubjectAdded(sub_addr, subjects[sub_addr].name);
    }
    //Push present time to history
    function push_history( address sub_addr,  uint256 current_time) public authorities_only{
        uint256 present_time = current_time % 86400;
        subjects[sub_addr].history.push(present_time);
    }
    // return the history
    function get_history(address sub_addr) public view returns(uint[] memory)  {
        return subjects[sub_addr].history;
    }
    // return subject's trust level
    function get_trust(address sub_addr) public view returns(uint)   {
        return subjects[sub_addr].trust;
     }
    // Adds a subject to bloom filter
    // By default hash_count is 5 in constructor
    // hash_count is number of times the sub_addr gets hashed
    function add_bitmap( /**SUBJECT ID**/address sub_addr )
    /**MODIFIERS**/
        internal
    {
        require(filter.hash_count > 0, "Hash count cannot be zero!");
        for(uint i = 0; i < filter.hash_count; i++) {
            uint256 index = uint256(keccak256(abi.encodePacked(sub_addr, i))) % 256;
            require(index < 256, "Overflow Error!");
            uint256 bit_place = 1 << index;
            filter.bitmap = filter.bitmap | bit_place;
        }
    }
    function set_subject_state(address sub_addr, Device.State  _state) public authorities_only(){
        subjects[sub_addr].state = _state;
    }
     // Check the sub_addr with the existing bloom filter
    // to see if sub_addr exists.
    // Returns true if sub_addr may exist
    // Returns false if sub_addr definitely doesn't exist
    function check_bitmap( /**SUBJECT ID**/ address sub_addr )/**MODIFIERS**/external view returns(bool)
    {
        require(filter.hash_count > 0, "Hash count cannot be zero");
        for(uint256 i = 0; i < filter.hash_count; i++){
            uint256 index = uint256(keccak256(abi.encodePacked(sub_addr, i))) % 256;
            require(index < 256, "Overflow Error!");
            uint256 bit_place = 1 << index;
            if((filter.bitmap & bit_place) == 0) return false;
        }
        return true;
    }

    // Changes the attributes of a subject
    // If attribute are blank "" skip to next attribute (no change done)
    // Note: Cannot set any attribute to empty string (blank)
    // Emits SubjectChanged event
    function change_attribs( 
        address sub_addr,         
        string memory name, // type of the device
        uint age, // Number of days since the device was first registered
        uint trust, // 1 to 100
        Device.Category category, 
        Device.Zone zone, // Location
        uint[] memory history, // history
        uint lastUpdated //lastime send request
         )  /**MODIFIERS**/ public authorities_only()  sub_active(sub_addr){
        bytes memory empty_name = bytes(name);  
        if (empty_name.length != 0) subjects[sub_addr].name = name;
        if (age != 0) subjects[sub_addr].age = age;
        if (trust != 0) subjects[sub_addr].trust = trust;
        if (category != Device.Category.Security) subjects[sub_addr].category = category;
        if (zone != Device.Zone.Zone1) subjects[sub_addr].zone = zone; 
        if (history.length != 0) subjects[sub_addr].history = history;
        if (lastUpdated != 0) subjects[sub_addr].lastUpdated = lastUpdated;
        
        emit SubjectChanged(sub_addr);

    }
}




    

        
    
