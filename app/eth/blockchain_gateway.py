from web3 import Web3
from pathlib import Path
from app.utils.path import (
    POOLS_JSON_PATH, 
    STAKING_JSON_PATH,
    FACTORY_JSON_PATH,
    ROUTER_JSON_PATH,
    TOKEN_JSON_PATH,
    PROVIDER_URL
)

from app.utils.addresses import CONTRACT_ADDRESSES

import json


class BaseContractClient:
    def __init__(self, json_contract_path: Path, contract_address: str):
        self.w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))
        self.public_key: str = None
        
        if not self.w3.is_connected:
            raise ConnectionError("HOOOOLY SHIT: No blockchain connection")
        
        with open(json_contract_path) as f:
            artifacts = json.load(f)
            
        self.contract = self.w3.eth.contract(
            address=self.w3.to_checksum_address(contract_address),
            abi=artifacts["abi"]
        )

factory_client = BaseContractClient(
    json_contract_path=FACTORY_JSON_PATH,
    contract_address=CONTRACT_ADDRESSES["factory"]
)

router_client = BaseContractClient(
    json_contract_path=ROUTER_JSON_PATH,
    contract_address=CONTRACT_ADDRESSES["router"]
)

staking_client = BaseContractClient(
    json_contract_path=STAKING_JSON_PATH,
    contract_address=CONTRACT_ADDRESSES["staking"]
)

poolKreRtk_client = BaseContractClient(
    json_contract_path=POOLS_JSON_PATH,
    contract_address=CONTRACT_ADDRESSES["pools"]["poolKreRtk"]
)

poolGerKre_client = BaseContractClient(
    json_contract_path=POOLS_JSON_PATH,
    contract_address=CONTRACT_ADDRESSES["pools"]["poolGerKre"]   
)