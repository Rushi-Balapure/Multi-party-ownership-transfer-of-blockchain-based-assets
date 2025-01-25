from web3 import Web3
import json
from solcx import compile_source, install_solc, set_solc_version
class BlockchainDeployment:
    def __init__(self):
    # Connect to Ganache
        self.ganache_url = "http://127.0.0.1:7545"  # Update with your Ganache RPC server
        self.web3 = Web3(Web3.HTTPProvider(self.ganache_url))

        # Check connection
        if not self.web3.is_connected():
            raise ConnectionError("Failed to connect to Ganache. Check your RPC URL.")

        # Set up default account
        self.web3.eth.default_account = self.web3.eth.accounts[0]  # First account in Ganache

        # Solidity contract file path
        self.contract_file_path = r"d:\Rushi\Coding\contract.sol"  # Use raw string or corrected path

        # Read Solidity contract from file
        with open(self.contract_file_path, "r") as file:
            self.contract_source_code = file.read()

        # Install and set Solidity compiler version
        install_solc("0.8.0")  # Install Solidity compiler version 0.8.0
        set_solc_version("0.8.0")  # Set the Solidity compiler version to use

        # Compile the contract
        self.compiled_sol = compile_source(self.contract_source_code)
        self.contract_interface = self.compiled_sol['<stdin>:TransactionSigner']

        # Deploy the contract
        self.TransactionSigner = self.web3.eth.contract(abi=self.contract_interface['abi'], bytecode=self.contract_interface['bin'])
        self.tx_hash = self.TransactionSigner.constructor().transact()
        self.tx_receipt = self.web3.eth.wait_for_transaction_receipt(self.tx_hash)

        # Get the deployed contract instance
        self.contract_instance = self.web3.eth.contract(
            address=self.tx_receipt.contractAddress,
            abi=self.contract_interface['abi']
        )

        print(f"Contract deployed at address: {self.tx_receipt.contractAddress}")

    # Interact with the contract
    def initiate_transaction_deploy(self,transaction_data, key):
        self.tx_hash = self.contract_instance.functions.initiateTransaction(transaction_data, key).transact()
        self.tx_receipt = self.web3.eth.wait_for_transaction_receipt(self.tx_hash)
        print(f"Transaction successful! Event logs: {self.tx_receipt['logs']}")

# # Test the contract
# transaction_data = "Transfer 100 tokens to address ABC123"
# reconstructed_key = "0x7f6e5d4c3b2a190807060504030201ffeeddccbbaa99887766554433221100ff"

# try:
#     initiate_transaction(transaction_data, reconstructed_key)
# except Exception as e:
#     print(f"Error during transaction: {e}")
