import time
import json
import web3
from eth_account import Account
from web3.auto import w3
from web3.providers.websocket import WebsocketProvider
from web3 import Web3
from solc import compile_standard

with open("cashback.sol") as c:
 contractText=c.read()
with open(".pk") as pkfile:
 privateKey=pkfile.read()
with open(".infura") as infurafile:
 infuraKey=infurafile.read()

compiled_sol = compile_source(contractText)
contract_id, contract_interface = compiled_sol.popitem()
bytecode = contract_interface['bin']
abi = contract_interface['abi']

W3 = Web3(WebsocketProvider('wss://ropsten.infura.io/ws/v3/%s'%infuraKey))
account1=Account.from_key(privateKey);
address1=account1.address

nonce = W3.eth.getTransactionCount(address1)
#diagnostics
#print(nonce)
# Submit the transaction that deploys the contract
tx_dict = cashback.constructor().buildTransaction({
  'chainId': 3,
  'gas': 1400000,
  'gasPrice': w3.toWei('40', 'gwei'),
  'nonce': nonce,
  'from':address1
})

signed_txn = W3.eth.account.sign_transaction(tx_dict, private_key=privateKey)
#diagnostics
#print(signed_txn)
print("Deploying the Smart Contract")
result = W3.eth.sendRawTransaction(signed_txn.rawTransaction)
#diagnostics
#print(result)
#print('-----------------------------------')
tx_receipt = None#W3.eth.getTransactionReceipt(result)

count = 0
while tx_receipt is None and (count < 30):
  time.sleep(10)
  try:
    tx_receipt = W3.eth.getTransactionReceipt(result)
  except:
    print('.')

if tx_receipt is None:
  print (" {'status': 'failed', 'error': 'timeout'} ")
#diagnostics
#print (tx_receipt)

print("Contract address is:",tx_receipt.contractAddress)
