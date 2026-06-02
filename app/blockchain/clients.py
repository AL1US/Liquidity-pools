from app.blockchain.blockchain_gateway import BaseContractClient

from app.utils.path import (
    POOLS_JSON_PATH, 
    STAKING_JSON_PATH,
    FACTORY_JSON_PATH,
    ROUTER_JSON_PATH,
    TOKEN_JSON_PATH
)

from app.utils.addresses import CONTRACT_ADDRESSES

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
gerda_client = BaseContractClient(
    json_contract_path=TOKEN_JSON_PATH,
    contract_address=CONTRACT_ADDRESSES["tokens"]["gerdaCoin"]   
)

krendel_client = BaseContractClient(
    json_contract_path=TOKEN_JSON_PATH,
    contract_address=CONTRACT_ADDRESSES["tokens"]["krendelCoin"]   
)

rtk_client = BaseContractClient(
    json_contract_path=TOKEN_JSON_PATH,
    contract_address=CONTRACT_ADDRESSES["tokens"]["rtkCoin"]   
)

professional_client = BaseContractClient(
    json_contract_path=TOKEN_JSON_PATH,
    contract_address=CONTRACT_ADDRESSES["tokens"]["professionalCoin"]   
)