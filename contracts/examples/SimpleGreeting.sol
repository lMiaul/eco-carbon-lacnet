// contracts/examples/SimpleGreeting.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SimpleGreeting {
    string public greeting;
    address public owner;

    event GreetingUpdated(string newGreeting, address updatedBy);

    constructor() {
        greeting = "Hello from Eco-Carbon San Martin on LACNet!";
        owner = msg.sender;
    }

    function updateGreeting(string memory _newGreeting) public {
        greeting = _newGreeting;
        emit GreetingUpdated(_newGreeting, msg.sender);
    }

    function getGreeting() public view returns (string memory) {
        return greeting;
    }
}
