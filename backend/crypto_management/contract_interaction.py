from web3 import Web3, HTTPProvider, IPCProvider
from os import path
import json


INFURA_URL = 'http://ropsten.infura.io/'


class ContractHandler:
    def __init__(self, contract_address):
        self.web3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/52a597c1982940f0b7367628415eeb8d"))
        self.contract_address = contract_address

        dir_path = path.dirname(path.realpath(__file__))
        with open(str(path.join(dir_path, 'contract_abi.json')), 'r') as abi_definition:
            self.abi = json.load(abi_definition)
        self.contract = self.web3.eth.contract(self.abi, self.contract_address)

    def create_agreement(self, addresses, signatures, timestamp):
        self.contract.call().createAgreement(
            addresses,
            signatures,
            timestamp
        )

# dir_path = path.dirname(path.realpath(__file__))
# web3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/52a597c1982940f0b7367628415eeb8d"))
# with open(str(path.join(dir_path, 'contract_abi.json')), 'r') as abi_definition:
    # abi = json.load(abi_definition)
# contract = web3.eth.contract(abi, contract_address)
