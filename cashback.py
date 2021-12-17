from solcx import install_solc
install_solc(version='latest')
from web3 import Web3
from solcx import compile_source
Solidity source code
# Solidity source code
compiled_sol = compile_source(

{
  // Defining a function to
  // return a string
  function get_output() public pure returns (string) 
  {
      return ("Hi, your contract ran successfully");
  }
}
# retrieve the contract interface
contract_id, contract_interface = compiled_sol.popitem()

# get bytecode / bin
bytecode = contract_interface['bin']

# get abi
abi = contract_interface['abi']

# web3.py instance
w3 = Web3(Web3.EthereumTesterProvider())

# set pre-funded account as sender
w3.eth.default_account = w3.eth.accounts[0]
    >>> Greeter = w3.eth.contract(abi=abi, bytecode=bytecode)

# Submit the transaction that deploys the contract
>>> tx_hash = Greeter.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

greeter = w3.eth.contract(
address=tx_receipt.contractAddress,
abi=abi
)

Greeter.functions.greet().call()
'Hello'

tx_hash = greeter.functions.setGreeting('Nihao').transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
greeter.functions.greet().call()
'Nihao'
