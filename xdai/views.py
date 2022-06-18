from django.shortcuts import render
from django.http import HttpResponse
from models.xEth import *
from models.config import *
from models.custom import *


w3 = initEthMainNet(xDai['url'])

"""
@apiDefine initRes
@apiSuccess {Number} data_status 返回码
@apiSuccess {String} msg 返回的msg
@apiSuccess {Object} results 返回的result结果
"""
def get_gas(request):

    """
    @api {POST} /xdai/get_gas 获取gas费
    @apiVersion 1.0.0
    @apiGroup xDai
    @apiDescription 获取xdai链gas费
    @apiSuccess {Number} data_status 返回码
    @apiSuccess {String} msg 返回的msg
    @apiSuccess {Object} results 返回的result结果
    @apiSuccessExample {Json} 成功返回案例
    {
        "stauts": 200,
        "msg": "success",
        "results": {
            "gas": 1000000000
        }
    }
    """

    result = w3.eth.gas_price
    return response(data_status=200, data_msg='success', gas=result)

def create_addr(request):

    """
    @api {POST} /xdai/create_addr 创建地址
    @apiDescription 创建xdai链地址
    @apiGroup xDai
    @apiVersion 1.0.0
    @apiUse initRes
    @apiSuccess {String} address 返回address
    @apiSuccess {String} privateKey 返回私钥
    @apiSuccessExample {Json} 成功返回案例
    {
        "stauts": 200,
        "msg": "success",
        "results": {
            "address": "0x3e26fc8fC1D9550294d4E86f36E5278ACb171BDC",
            "privateKey": "0x1d2becc94c72e561327b009c28f3f3ce638cd6e55692e6c5862fb3955141e6cf"
        }
    }
    """

    account = w3.eth.account.create()
    return response(data_status=200, data_msg='success', address=account.address, privateKey=str(account.key.hex).split("'")[1])


@getArgs
def transfer(args):

    """
    @api {POST} /xdai/transfer 创建交易
    @apiDescription 创建xdai链交易（非erc20）
    @apiGroup xDai
    @apiVersion 1.0.0
    @apiUse initRes
    @apiParam {Number} [gas=1000000000/GWei] gas费，默认为会自动获取，可不传，当需要替换交易时可考虑传入该参数，并且数值大于正常gas费
    @apiParam {Number} [nonce] addr地址的最新交易id，默认为会自动获取，可不传，当需要替换交易时必须传入该参数，并且应为需替换的交易的nonce值
    @apiParam {String} from_addr 转出交易的源地址，必传
    @apiParam {String} to_addr 转出交易的目标地址，必传
    @apiParam {Number} amount 转出交易的金额数量，必传
    @apiParam {String} priv_key 源地址对应的私钥，必传
    @apiSuccess {String} txid 返回交易成功之后的txid
    @apiParamExample {json} 请求案例
    {
        "from_addr": "0x31a24fEFE2B4E595505021E42c797E0eecAfccB1",
        "to_addr": "0x99aF1303b692e3A502ff57f99BdDb4eD0CbBA475",
        "amount": 0.1,
        "priv_key": "2601098255ce*************************1378a4c837f8733631e"
    }
    @apiSuccessExample {Json} 成功返回案例
    {
        "stauts": 200,
        "msg": "success",
        "results": {
            "txid": "0x4c0b7d33b21e851c393d282460614ea5570bf7c95498116c8ca4dc2882c5af02"
        }
    }
    """

    from_addr = w3.toChecksumAddress(args['from_addr'])
    to_addr = w3.toChecksumAddress(args['to_addr'])

    if 'gas' not in args.keys():
        args['gas'] = w3.eth.gas_price

    if 'nonce' not in args.keys():
        args['nonce'] = getNonce(addr=from_addr, w3=w3)

    amount_value = w3.toWei(args['amount'], 'ether')
    sig_tx = w3.eth.account.sign_transaction(dict(
        nonce=args['nonce'],
        gasPrice=args['gas'],
        gas=2000000,
        to=to_addr,
        value=amount_value,
        # data=b'',
    ),
        args['priv_key'],
    )
    reslut = w3.eth.send_raw_transaction(sig_tx.rawTransaction).hex()
    return response(data_status=200, data_msg='success', txid=reslut)

@getArgs
def get_balance(args):
    """
    @api {POST} /xdai/get_balance 获取余额
    @apiDescription 获取账户余额（非erc20）
    @apiGroup xDai
    @apiVersion 1.0.0
    @apiUse initRes
    @apiParam {String} addr 需查询的账户地址
    @apiSuccess {Number} balance 返回查询地址的余额
    @apiParamExample {json} 请求案例
    {
        "addr": "0x31a24fEFE2B4E595505021E42c797E0eecAfccB1",
    }
    @apiSuccessExample {Json} 成功返回案例
    {
        "stauts": 200,
        "msg": "success",
        "results": {
            "balance": "0.49933436"
        }
    }
    """

    addr = w3.toChecksumAddress(args['addr'])

    balance = w3.fromWei(w3.eth.get_balance(addr), 'ether')
    return response(data_status=200, data_msg='success', balance=balance)

@getArgs
def get_nonce(args):
    """
    @api {POST} /xdai/get_nonce 获取nonce
    @apiDescription 获取传入账户的最新nonce值
    @apiGroup xDai
    @apiVersion 1.0.0
    @apiUse initRes
    @apiParam {String} addr 需查询的账户地址
    @apiSuccess {Number} nonce 返回查询地址的nonce值
    @apiSuccess {String} addr 返回查询地址
    @apiParamExample {json} 请求案例
    {
        "addr": "0x31a24fEFE2B4E595505021E42c797E0eecAfccB1",
    }
    @apiSuccessExample {Json} 成功返回案例
    {
        "stauts": 200,
        "msg": "success",
        "results": {
            "addr": "0x31a24fEFE2B4E595505021E42c797E0eecAfccB1",
            "nonce": 28
        }
    }
    """

    addr = w3.toChecksumAddress(args['addr'])

    nonce = getNonce(addr=addr, w3=w3)
    return response(data_status=200, data_msg='success', addr=addr, nonce=nonce)

@getArgs
def get_erc20_blance(args):
    """
    @api {POST} /xdai/get_erc20_blance 获取ERC20余额
    @apiDescription 获取账户ERC20某代币合约余额
    @apiGroup xDai
    @apiVersion 1.0.0
    @apiUse initRes
    @apiParam {String} addr 需查询的账户地址
    @apiParam {String} contract_addr 需查询的对应代币的合约地址
    @apiSuccess {Number} balance 返回查询地址的余额
    @apiSuccess {String} addr 查询的账户地址
    @apiSuccess {String} contract_addr 查询的代币合约
    @apiParamExample {json} 请求案例
    {
        "addr": "0x99aF1303b692e3A502ff57f99BdDb4eD0CbBA475",
        "contract_addr": "0xdBF3Ea6F5beE45c02255B2c26a16F300502F68da"
    }
    @apiSuccessExample {Json} 成功返回案例
    {
        "stauts": 200,
        "msg": "success",
        "results": {
            "addr": "0x99aF1303b692e3A502ff57f99BdDb4eD0CbBA475",
            "contract_addr": "0xdBF3Ea6F5beE45c02255B2c26a16F300502F68da",
            "balance": 2
        }
    }
    """

    addr = w3.toChecksumAddress(args['addr'])

    EIP20_ABI = json.loads(EIP20)
    con_addr = w3.eth.contract(address=args['contract_addr'], abi=EIP20_ABI)
    decimals = con_addr.functions.decimals().call()
    DECIMALS = 10 ** decimals
    balance = con_addr.functions.balanceOf(addr).call() / DECIMALS
    return response(data_status=200, data_msg='success', addr=addr, contract_addr=args['contract_addr'], balance=balance)


@getArgs
def erc20_transfer(args):
    """
    @api {POST} /xdai/erc20_transfer 创建ERC20交易
    @apiDescription 创建xdai链ERC20交易
    @apiGroup xDai
    @apiVersion 1.0.0
    @apiUse initRes
    @apiParam {Number} [gas=1000000000/GWei] gas费，默认为会自动获取，可不传，当需要替换交易时可考虑传入该参数，并且数值大于正常gas费
    @apiParam {Number} [nonce] addr地址的最新交易id，默认为会自动获取，可不传，当需要替换交易时必须传入该参数，并且应为需替换的交易的nonce值
    @apiParam {String} from_addr 转出交易的源地址，必传
    @apiParam {String} to_addr 转出交易的目标地址，必传
    @apiParam {Number} amount 转出交易的金额数量，必传
    @apiParam {Number} contract_addr 对应erc20合约地址，必传
    @apiParam {String} priv_key 源地址对应的私钥，必传
    @apiSuccess {String} txid 返回交易成功之后的txid
    @apiParamExample {json} 请求案例
    {
        "from_addr": "0x31a24fEFE2B4E595505021E42c797E0eecAfccB1",
        "to_addr": "0x99aF1303b692e3A502ff57f99BdDb4eD0CbBA475",
        "amount": 0.1,
        "contract_addr": "0xdBF3Ea6F5beE45c02255B2c26a16F300502F68da",
        "priv_key": "2601098255ce*************************1378a4c837f8733631e"
    }
    @apiSuccessExample {Json} 成功返回案例
    {
        "stauts": 200,
        "msg": "success",
        "results": {
            "txid": "0x4c0b7d33b21e851c393d282460614ea5570bf7c95498116c8ca4dc2882c5af02"
        }
    }
    """

    from_addr = w3.toChecksumAddress(args['from_addr'])
    to_addr = w3.toChecksumAddress(args['to_addr'])

    if 'gas' not in args.keys():
        args['gas'] = w3.eth.gas_price

    if 'nonce' not in args.keys():
        args['nonce'] = getNonce(addr=from_addr, w3=w3)

    EIP20_ABI = json.loads(EIP20)
    con_addr = w3.eth.contract(address=args['contract_addr'], abi=EIP20_ABI)
    decimals = con_addr.functions.decimals().call()
    DECIMALS = 10 ** decimals
    trans = con_addr.functions.transfer(
        to_addr,
        int(args['amount']) * DECIMALS,
    ).buildTransaction({
        'chainId': xDai['chainId'],
        'nonce': args['nonce'],
        'gasPrice': args['gas'],
        'gas': 2000000,
        'value': 0,
    })
    signed_txn = w3.eth.account.sign_transaction(trans, args['priv_key'])
    reslut = w3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()
    return response(data_status=200, data_msg='success', txid=reslut)

@getArgs
def get_block(args):
    """
    @api {POST} /xdai/get_block 获取块详情
    @apiDescription 获取某一个区块的元数据信息
    @apiGroup xDai
    @apiVersion 1.0.0
    @apiUse initRes
    @apiParam {Number} [blkNum] 需查询的区块号
    @apiParam {String} [blkHash] 需查询的区块hash，同时传入blkNum，blkNum优先请注意，如果都不传，则获取最新的一个区块信息
    @apiParamExample {json} 请求案例
    {
        "blkNum": 123456,
    }
    @apiSuccessExample {Json} 成功返回案例
    {
        "stauts": 200,
        "msg": "success",
        "results": "AttributeDict({'author': '0x9233042b8e9e03d5dc6454bbbe5aee83818ff103', 'difficulty': 340282366920938463463374607431768211454, 'proofOfAuthorityData': HexBytes('0xde830201018f5061726974792d457468657265756d86312e32392e30826c69'), 'gasLimit': 10000000, 'gasUsed': 0, 'hash': HexBytes('0xb4036fb5ba6d8c55c92f129435fa7a6077bff3478889bde25529d38457ced184'), 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'), 'miner': '0x9233042B8E9E03D5DC6454BBBe5aee83818fF103', 'number': 123456, 'parentHash': HexBytes('0xfd4b7b9ef71d0c4e6766dfac742a3892f88fb348a951a39d0c062a8709e1b930'), 'receiptsRoot': HexBytes('0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421'), 'sha3Uncles': HexBytes('0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347'), 'signature': '0x9153f2aefbca44e2f8ad91023df7bfd0519d19fd2016a97d98ec4e9bf69ca88c297853533549247fba932736bd17961a7fcd787c664973a18754a8ba5bf63b1a00', 'size': 588, 'stateRoot': HexBytes('0x52978337c6ffb9d541b3c8d5e40fafcbaaef9157811161f8b5b3c436372abda0'), 'step': 307928341, 'totalDifficulty': 42009899890591378945334375535096376005591211, 'timestamp': 1539641705, 'transactions': [], 'transactionsRoot': HexBytes('0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421'), 'uncles': []})"
    }
    """

    if 'blkNum' in args.keys():
        result = w3.eth.get_block(args['blkNum'])
    elif 'blkHash' in args.keys():
        result = w3.eth.get_block(args['blkHash'])
    else:
        result = w3.eth.get_block('latest')

    return response(data_status=200, data_msg='success', results=result)

def get_latest_blkNum(request):
    """
    @api {POST} /xdai/get_latest_blkNum 获取最新块高
    @apiDescription 获取最新的块高
    @apiGroup xDai
    @apiVersion 1.0.0
    @apiUse initRes
    @apiSuccess {integer} latest_block_number 当前最新的区块高度
    @apiSuccessExample {Json} 成功返回案例
    {
        "stauts": 200,
        "msg": "success",
        "results": {
            "latest_block_number": 18875788
        }
    }
    """

    blkNum = w3.eth.block_number
    return response(data_status=200, data_msg='success', latest_block_number=blkNum)

@getArgs
def get_transcation(args):
    """
    @api {POST} /xdai/get_transcation 查询交易
    @apiDescription 查询某一个交易txid详情
    @apiGroup xDai
    @apiVersion 1.0.0
    @apiUse initRes
    @apiParam {String} txHash 需查询的交易hash
    @apiParamExample {json} 请求案例
    {
        "txHash": "0x4c0b7d33b21e851c393d282460614ea5570bf7c95498116c8ca4dc2882c5af02",
    }
    @apiSuccessExample {Json} 成功返回案例
    {
        "stauts": 200,
        "msg": "success",
        "results": "AttributeDict({'hash': HexBytes('0x4c0b7d33b21e851c393d282460614ea5570bf7c95498116c8ca4dc2882c5af02'), 'nonce': 27, 'blockHash': HexBytes('0x41e10d25752ca882ba76cf6e89c9f5e14effe1c4be10e02c9c702ae5e38b7ea7'), 'blockNumber': 18864200, 'transactionIndex': 9, 'from': '0x31a24fEFE2B4E595505021E42c797E0eecAfccB1', 'to': '0x99aF1303b692e3A502ff57f99BdDb4eD0CbBA475', 'value': 100000000000000000, 'gasPrice': 1000000000, 'gas': 2000000, 'data': '0x', 'input': '0x', 'type': '0x0', 'v': 27, 's': HexBytes('0x3e10b2de30608841fa1b9504c5682a9d5bde1b33f11a90fd5b4ff63406ffbc8c'), 'r': HexBytes('0x6f53a91e308f7a59263be3d479e709733ff0a2f3919431c69452ad71a38cd0f6')})"
    }
    """
    result =w3.eth.get_transaction(transaction_hash=args['txHash'])
    return response(data_status=200, data_msg='success', results=result)

@getArgs
def replace_transfer(args):
    """
    @api {POST} /xdai/replace_transfer 替换交易
    @apiDescription 替换xdai链交易（包含ERC20）
    @apiGroup xDai
    @apiVersion 1.0.0
    @apiUse initRes
    @apiParam {Number} [gas=1000000000/GWei] gas费，默认为会自动获取，可不传，当需要替换交易时可考虑传入该参数，并且数值大于正常gas费
    @apiParam {Number} nonce 必传，应为账户地址需替换的交易的nonce值
    @apiParam {String} from_addr 转出交易的源地址，必传
    @apiParam {String} to_addr 转出交易的目标地址，必传
    @apiParam {Number} amount 转出交易的金额数量，必传
    @apiParam {Number} [contract_addr] 可选，当替换erc20交易时，需传入
    @apiParam {String} priv_key 源地址对应的私钥，必传
    @apiSuccess {String} txid 返回替换成功之后的txid
    @apiParamExample {json} 请求案例
    {
        "from_addr": "0x31a24fEFE2B4E595505021E42c797E0eecAfccB1",
        "to_addr": "0x99aF1303b692e3A502ff57f99BdDb4eD0CbBA475",
        "amount": 0.1,
        "nonce": 28,
        "contract_addr": "0xdBF3Ea6F5beE45c02255B2c26a16F300502F68da",
        "priv_key": "2601098255ce*************************1378a4c837f8733631e"
    }
    @apiSuccessExample {Json} 成功返回案例
    {
        "stauts": 200,
        "msg": "success",
        "results": {
            "txid": "0x4c0b7d33b21e851c393d282460614ea5570bf7c95498116c8ca4dc2882c5af02"
        }
    }
    """

    if args['contract_addr'] and args['nonce']:
        return erc20_transfer(args=args)
    elif args['nonce']:
        return transfer(args=args)
    return response(data_status=666, data_msg='faild', results='args is wrong, please look apidoc')

