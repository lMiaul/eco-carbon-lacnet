// contracts/examples/SimpleStorage.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SimpleStorage {
    mapping(string => uint256) private carbonData;
    mapping(address => bool) public authorizedWriters;
    address public admin;

    event DataStored(string key, uint256 value, address storedBy);

    constructor() {
        admin = msg.sender;
        authorizedWriters[msg.sender] = true;
    }

    function storeCarbonData(string memory key, uint256 value) public {
        require(authorizedWriters[msg.sender], "Not authorized");
        carbonData[key] = value;
        emit DataStored(key, value, msg.sender);
    }

    function getCarbonData(string memory key) public view returns (uint256) {
        return carbonData[key];
    }

    function authorizeWriter(address writer) public {
        require(msg.sender == admin, "Only admin can authorize");
        authorizedWriters[writer] = true;
    }
}
