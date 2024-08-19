// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;
import "contracts/Device.sol";
contract ObjectAttribute {
    struct Object {
        Device.State state;
        string name; // type od the device
        uint age; // Number of days since the device was first registered
        uint trust; // 1 to 10
        Device.Category category; 
        Device.Zone zone; // Location
    }
    struct BloomFilter {
        uint256 bitmap;
        uint8 hash_count; 
    }
    // local variables
    mapping(address => bool) public authorities;
    uint256 num_objects;
    BloomFilter filter;
    address[] users;

    //mapping addresses of objects
    mapping (address => Object) public objects;

    constructor() {
        authorities[msg.sender] = true;
        num_objects = 0;
        filter.bitmap = 0;
        filter.hash_count = 5;
    }

    //Authorities Only
    modifier authorities_only(){
        require(authorities[msg.sender] == true, "Sender is not an authority.");
        _;
    }
    modifier obj_active(address obj_addr){
        require(objects[obj_addr].state == Device.State.Active, "Object statee is not active!");
        _;
    }
    // Events
    event NewObjectAdded(address obj_addr, string name);
    event ObjectChanged(address sub_addr, string name);

    function addAuthority(address authority) public authorities_only() {
        authorities[authority] = true;
    }

    //Adding an Object
    function add_object (
        address obj_addr,         
        string memory name, // type of the device
        uint trust, // 1 to 10
        Device.Category category, 
        Device.Zone zone // Location
        ) public authorities_only() {

        num_objects++;
        objects[obj_addr].state = Device.State.Active;
        //Subject Attributes:
        objects[obj_addr].name = name;
        objects[obj_addr].age = block.timestamp;
        objects[obj_addr].trust = trust;
        objects[obj_addr].category = category;
        objects[obj_addr].zone = zone;

        add_bitmap(obj_addr);

        emit NewObjectAdded(obj_addr, objects[obj_addr].name);
        
        }

    // Adds a subject to bloom filter
    // By default hash_count is 5 in constructor
    // hash_count is number of times the ob_addr gets hashed
    function add_bitmap(  /**SUBJECT ID**/ address sub_addr)internal {
         require(filter.hash_count > 0, "Hash count cannot be zero!");
        for(uint i = 0; i < filter.hash_count; i++) {
            uint256 index = uint256(keccak256(abi.encodePacked(sub_addr, i))) % 256;
            require(index < 256, "Overflow Error!");
            uint256 bit_place = 1 << index;
            filter.bitmap = filter.bitmap | bit_place;
        }    
    }
    function check_bitmap( /**OBJECT ID**/ address obj_addr )/**MODIFIERS**/external view returns(bool)
    {
        require(filter.hash_count > 0, "Hash count cannot be zero");
        for(uint256 i = 0; i < filter.hash_count; i++){
            uint256 index = uint256(keccak256(abi.encodePacked(obj_addr, i))) % 256;
            require(index < 256, "Overflow Error!");
            uint256 bit_place = 1 << index;
            if((filter.bitmap & bit_place) == 0) return false;
        }
        return true;
    }
    // Change Object's state
    function set_object_state(address obj_addr, Device.State  _state) public authorities_only(){
        objects[obj_addr].state = _state;
    }
    // Changes the attributes of a subject
    // If attribute are blank "" skip to next attribute (no change done)
    // Note: Cannot set any attribute to empty string (blank)
    // Emits SubjectChanged event
    function change_attribs( 
        address obj_addr,         
        string memory name, // type of the device
        uint age, // Number of days since the device was first registered
        uint trust, // 1 to 10
        Device.Category category, 
        Device.Zone zone // Location
         )  /**MODIFIERS**/ public authorities_only()  obj_active(obj_addr){
        bytes memory empty_test = bytes(name);  
        if (empty_test.length != 0) objects[obj_addr].name = name;
        if (age != 0) objects[obj_addr].age = age;
        if (trust != 0) objects[obj_addr].trust = trust;
        if (category != Device.Category.Security) objects[obj_addr].category = category;
        if (zone != Device.Zone.Zone1) objects[obj_addr].zone = zone; 
         
        emit ObjectChanged(obj_addr,objects[obj_addr].name );

    }
}