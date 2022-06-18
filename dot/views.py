from django.shortcuts import render
from models.DOT import *
from models.custom import *

substrate = initDOT('polkadot')

@getArgs
def transfer(args):

    keypair = Keypair.create_from_private_key(args['priv_key'])
    call = substrate.compose_call(
        call_module='Balances',
        call_function='transfer',
        call_params={
            'dest': args['to_addr'],
            'value': 1 * 10 ** substrate.properties['tokenDecimals']
        }
    )

    if 'nonce' not in args.keys():
        extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)
    else:
        extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair, nonce=args['nonce'])

    try:
        result = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        return response(data_status=200, data_msg='success', txid=result)

    except Exception as e:
        return response(data_status=500, data_msg='faild', msg='extrinsic send faild, please send again.')


@getArgs
def get_accountInfo(args):

    result = substrate.query(
        module='System',
        storage_function='Account',
        params=[args['addr']]
    )

    return response(data_status=200, data_msg='success', addr=args['addr'], result=result.value)


def create_addr(request):

    mnemonic = Keypair.generate_mnemonic()
    result = Keypair.create_from_mnemonic(mnemonic)

    return response(data_status=200, data_msg='success', address=result.ss58_address, mnemonic=result.mnemonic)

@getArgs
def get_block(args):

    result = substrate.get_block(block_number=args['blkNum'])

    return response(data_status=200, data_msg='success', results=result)


def get_latest_blkNum(request):

    result = substrate.get_block_number(substrate.get_chain_head())

    return response(data_status=200, data_msg='success', latest_block_number=result)

