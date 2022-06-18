from web3 import Web3
import requests, json
from web3.middleware import geth_poa_middleware

def initEthMainNet(url):
    node = Web3.HTTPProvider(url)
    w3 = Web3(node)
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    w3.eth.account.enable_unaudited_hdwallet_features()
    return w3


def getNonce(addr, w3, **args):
    nonce = w3.eth.get_transaction_count(addr, 'pending')
    return nonce