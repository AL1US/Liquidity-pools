import json
from pathlib import Path
from typing import Optional, List, Any
from web3 import Web3


ETH_DIR = Path(__file__).resolve().parent
BLOCKCHAIN_DIR = ETH_DIR / "../../blockchain" 

BASE_DIR = BLOCKCHAIN_DIR / "artifacts/contracts"
ADDRESSES_JSON_PATH = BLOCKCHAIN_DIR / "addresses/addresses.json"

PROVIDER_URL = "http://127.0.0.1:8545"

with open(ADDRESSES_JSON_PATH, "r") as f:
    CONTRACT_ADDRESSES = json.load(f)

class BaseContractClient:
    def __init__(self, json_contract_path: Path, contract_address: str):
        self.w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))
        self.public_key: Optional[str] = None
        
        if not self.w3.is_connected():
            raise ConnectionError("HOOOOLY SHIT: No blockchain connection")
        print(f"CONNECTED TO NETWORK for contract at {contract_address[:10]}...")
            
        with open(json_contract_path) as f:
            artifact = json.load(f)
            
        self.contract = self.w3.eth.contract(
            address=self.w3.to_checksum_address(contract_address),   
            abi=artifact["abi"]
        )

factory_client = BaseContractClient(
    json_contract_path=BASE_DIR / "Factory.sol/Factory.json",
    contract_address=CONTRACT_ADDRESSES["factory"]
)

router_client = BaseContractClient(
    json_contract_path=BASE_DIR / "Router.sol/Router.json",
    contract_address=CONTRACT_ADDRESSES["router"]
)

staking_client = BaseContractClient(
    json_contract_path=BASE_DIR / "Staking.sol/Staking.json",
    contract_address=CONTRACT_ADDRESSES["staking"]
)

poolKreRtk_client = BaseContractClient(
    json_contract_path=BASE_DIR / "Pools.sol/Pool.json",
    contract_address=CONTRACT_ADDRESSES["pools"]["poolKreRtk"]
)

poolGerKre_client = BaseContractClient(
    json_contract_path=BASE_DIR / "Pools.sol/Pool.json",
    contract_address=CONTRACT_ADDRESSES["pools"]["poolGerKre"]
)