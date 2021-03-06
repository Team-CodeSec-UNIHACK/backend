#!/usr/bin/env python
from web3 import Web3, HTTPProvider
import json
import binascii
from web3.middleware import geth_poa_middleware


def save_to_blockchain(provider_url, data, sender_addr, sender_private_key, to_address, contract_address ):

    w3 = Web3(Web3.HTTPProvider(provider_url))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    # w3.isConnected()

    abi = '[{"constant":true,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"},{"name":"_releaseTime","type":"uint256"}],"name":"mintTimelocked","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]'
    abi = json.loads(abi)
    # Contract address
    dai = w3.eth.contract(address=contract_address, abi=abi)
    balance = w3.eth.get_balance(sender_addr)
    #  Receiver(Bharath)

    nonce = w3.eth.getTransactionCount(sender_addr)

    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': w3.toWei(0.000001, 'ether'),
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei'),
        'data': data.encode("utf-8").hex()
    }
    signed_tx = w3.eth.account.signTransaction(tx, sender_private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_id   = w3.toHex(tx_hash)
    return tx_id


def do_save_to_blockchain(data):
    url = "https://rinkeby.infura.io/v3/c1f318b7993a428e8c47d5167175465c"
    sender_addr = '0x2a6aF750B77daAb64fF3921EAb03f4de067C0883'
    sender_private_key = '0x21293aa392fcf8bf85f8a00171d6ab8a62405178a5845468707f7bd0377f7c4b'
    to_address = "0x12E9234Ac5fBa13A30E548F618d747c91C7768a1"
    contract_address = '0xd26114cd6EE289AccF82350c8d8487fedB8A0C07'

    return save_to_blockchain(url, data, sender_addr, sender_private_key, to_address, contract_address)

tx_id = do_save_to_blockchain("this is another test")
print(tx_id)