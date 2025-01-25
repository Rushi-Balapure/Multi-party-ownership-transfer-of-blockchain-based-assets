// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TransactionSigner {
    // Event to log the signed transaction
    event TransactionInitiated(address indexed initiator, string transactionData, bytes32 signedHash);

    // Function to initiate a transaction by signing it with a key
    function initiateTransaction(string memory transactionData, bytes16 key) public {
        require(bytes(transactionData).length > 0, "Transaction data cannot be empty.");
        require(key != bytes32(0), "Key cannot be empty.");

        // Simulate signing by hashing the transaction data and key
        bytes32 signedHash = keccak256(abi.encodePacked(transactionData, key));

        // Emit an event to log the signed transaction
        emit TransactionInitiated(msg.sender, transactionData, signedHash);
    }
}
