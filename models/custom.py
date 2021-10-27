from django.http import JsonResponse
from web3 import Web3
import requests, json
from web3.middleware import geth_poa_middleware

def initEthMainNet(url):
    node = Web3.HTTPProvider(url)
    w3 = Web3(node)
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

def getArgs(func):

    def returnFunc(request):
        from_addr = request.GET['from_addr']
        to_addr = request.GET['to_addr']
        priv_key = request.GET['priv_key']
        amount = request.GET['amount']
        addr = request.GET['addr']
        contract_addr = request.GET['contract_addr']
        blkNum = request.GET['blkNum']
        blkHash = request.GET['blkHash']

        return func(from_addr=from_addr, to_addr=to_addr, priv_key=priv_key, amount=amount, addr=addr, contract_addr=contract_addr, blkNum=blkNum, blkHash=blkHash)
    return returnFunc

def getNonce(addr, w3, **args):
    nonce = w3.eth.get_transaction_count(addr, 'pending')
    return nonce

def response(data_status=0, data_msg='ok', results=None,http_status=None, headers=None, exception=False, **kwargs):
    data = {
        'stauts': data_status,
        'msg': data_msg,
    }
    if results is not None:
        data['results'] = results
    data.update(kwargs)
    return JsonResponse(data)
