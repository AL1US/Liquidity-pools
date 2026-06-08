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
