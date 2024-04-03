//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract FundTransfer {
    address payable public owner; // Address set to payable in order to let it receive or send Ether
    uint public value;

    // Constructor function through which the smart contract can be created
    constructor() payable { // Also in this case, the function is payable
        owner = payable(msg.sender);
        value = uint(msg.value);
    }

    // Main function of the smart contract with two parameters
    function ConditionalTransaction(address recipient, uint currentValue) external {
        if(currentValue < 800) {
            TransferWhenMet(recipient); // TransferWhenMet is activated when currentValue is lower than 800
            } else {
                withdrawEthereum(); // While, when currentValue is higher or equal than 800, the withdrawEthereum gets triggered
                }
    }

    function TransferWhenMet(address recipient) public {
        require(address(this).balance > 0, "Contract has no funds"); // The balance of the smart contract has to be higher than 0 for the Ether to be sent
        (bool success, ) = payable(recipient).call{value: address(this).balance}("");
        require(success, "Transaction failed"); // This require function shows whether TransferWhenMet was successful or not
    }

    function withdrawEthereum() public {
        require(msg.sender == owner, "Withdraw possible only for the owner"); // The withdraw function can be triggered only by the owner of the smart contract (sender_address)
        payable(msg.sender).transfer(address(this).balance);
        }

    receive() external payable { // Fallback function
    }
}