import json
from web3 import Web3

infura_url = 'https://mainnet.infura.io/v3/0c23c4378d26402fb5e8a2e5cd2d9c6a'
web3 = Web3(Web3.HTTPProvider(infura_url))

abi = json.loads('[{"constant": true,"inputs": [],"name": "get_output","outputs": [{"name": "","type": "string"}],"payable": false,"stateMutability": "view","type": "function}]')

address = '0xf6b15DF3BaC48e94C23CcA42bfC83f870455bCa8'


contract = web3.eth.contract(address=address, abi=abi)

#need to put .call() at the end to call the smart contract
totalSupply = contract.functions.totalSupply().call()
print(" ")
print("Reading the smart contract from etherium node....")
#convert supply to Wei witch is 18 decimal places)

print(" ")
print('Total Supply: ', totalSupply/1000000)
print(" ")
print('Smart Contract Name: ', contract.functions.name().call())
print(" ")
print('Symbol: ', contract.functions.symbol().call())


		 \
