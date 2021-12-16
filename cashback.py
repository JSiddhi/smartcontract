import time
from web3 import Web3, HTTPProvider

contract_address     = [0x25338e1e162a9d3f8F4be67633277d5DfcACa9Eb]
wallet_private_key   = [db4f93c1ea15afb1db3f5ca216931597f0065fb0d730818c200727591ae97e]
wallet_address       = [0xf6b15DF3BaC48e94C23CcA42bfC83f870455bCa8]

w3 = Web3(HTTPProvider([0c23c4378d26402fb5e8a2e5cd2d9c6a]))

w3.eth.enable_unaudited_features()

contract = w3.eth.contract(address = contract_address, abi = contract_abi.abi)

def send_ether_to_contract(amount_in_ether):

    amount_in_wei = w3.toWei(amount_in_ether,'ether');

    nonce = w3.eth.getTransactionCount(wallet_address)

    txn_dict = {
            'to': contract_address,
            'value': amount_in_wei,
            'gas': 2000000,
            'gasPrice': w3.toWei('40', 'gwei'),
            'nonce': nonce,
            'chainId': 3
    }

    signed_txn = w3.eth.account.signTransaction(txn_dict, wallet_private_key)

    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    txn_receipt = None

    count = 0
    while txn_receipt is None and (count < 30):

        txn_receipt = w3.eth.getTransactionReceipt(txn_hash)

        print(txn_receipt)

        time.sleep(10)


    if txn_receipt is None:
        return {'status': 'failed', 'error': 'timeout'}

    return {'status': 'added', 'txn_receipt': txn_receipt}


def check_whether_address_is_approved(address):

    return contract.functions.isApproved(address).call()


def broadcast_an_opinion(covfefe):

    nonce = w3.eth.getTransactionCount(wallet_address)

    txn_dict = contract.functions.broadcastOpinion(covfefe).buildTransaction({
        'chainId': 3,
        'gas': 140000,
        'gasPrice': w3.toWei('40', 'gwei'),
        'nonce': nonce,
    })

    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)

    result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    tx_receipt = w3.eth.getTransactionReceipt(result)

    count = 0
    while tx_receipt is None and (count < 30):

        time.sleep(10)

        tx_receipt = w3.eth.getTransactionReceipt(result)

        print(tx_receipt)


    if tx_receipt is None:
        return {'status': 'failed', 'error': 'timeout'}

    processed_receipt = contract.events.OpinionBroadcast().processReceipt(tx_receipt)

    print(processed_receipt)

    output = "Address {} broadcasted the opinion: {}"\
        .format(processed_receipt[0].args._soapboxer, processed_receipt[0].args._opinion)
    print(output)

    return {'status': 'added', 'processed_receipt': processed_receipt}

if __name__ == "__main__":

    send_ether_to_contract(0.03)

    is_approved = check_whether_address_is_approved(wallet_address)
    
    print(is_approved)

    broadcast_an_opinion('Despite the Constant Negative Press')
