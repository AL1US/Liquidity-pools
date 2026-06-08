from app.blockchain.clients import (
    gerda_client,
    krendel_client,
    rtk_client,
    professional_client
)
TOKEN_DICT = {
    "gerda_client": gerda_client,
    "krendel_client": krendel_client,
    "rtk_client": rtk_client,
    "professional_client": professional_client
}

TOKEN_MAPPING = {
    gerda_client.contract.address.lower(): gerda_client,
    krendel_client.contract.address.lower(): krendel_client,
    rtk_client.contract.address.lower(): rtk_client,
    professional_client.contract.address.lower(): professional_client,
}