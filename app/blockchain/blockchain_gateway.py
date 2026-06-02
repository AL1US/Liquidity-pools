from web3 import Web3
from pathlib import Path
from app.utils.path import PROVIDER_URL


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
