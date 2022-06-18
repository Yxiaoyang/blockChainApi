#!/usr/bin/python3
# https://github.com/polkascan/py-substrate-interface
from substrateinterface import *
from scalecodec.type_registry import load_type_registry_file, SUPPORTED_TYPE_REGISTRY_PRESETS
from models.config import *
import sys


def initDOT(chainName):

    '''
    初始化 波卡生态 接口
    :param chainName: 波卡生态下的链名称
    :return substrate: 返回已获取的接口对象
    '''

    chainConf = {
        'crust': crust,
        'polkadot': polkadot,
        'kusama': kusama
    }

    if chainName not in SUPPORTED_TYPE_REGISTRY_PRESETS:
        custom_type_registry = load_type_registry_file(chainConf[chainName]['type_registry_file'])
        chainConf[chainName]['type_registry'] = custom_type_registry

    substrate = SubstrateInterface(
        url=chainConf[chainName]['url'],
        ss58_format=chainConf[chainName]['ss58_format'],
        type_registry_preset=chainConf[chainName]['type_registry_preset'],
        type_registry=chainConf[chainName]['type_registry']
    )

    return substrate
