import pathlib

from terra_sdk.client.lcd import LCDClient
from terra_sdk.core import Dec
from terra_sdk.core.coin import Coin

from anchorman.anchor import (
    amount_deposited_in_earn,
    PUBLIC_NODE_URLS,
    mnem_key_from_file,
)

HERE = pathlib.Path(__file__).parent.resolve()
ROOT = HERE.parent

CHAIN_ID_TESTNET = "tequila-0004"
LCD_TEST = LCDClient(chain_id=CHAIN_ID_TESTNET, url=PUBLIC_NODE_URLS[CHAIN_ID_TESTNET])
MNEM_PATH_TEST = ROOT / "mnemonic.txt"
WALLET_TEST = LCD_TEST.wallet(mnem_key_from_file(MNEM_PATH_TEST))


def test_amount_deposited_in_earn():
    EXPECTED_AMOUNT_IN_EARN = Coin("uusd", Dec(1597.783021))

    amount_in_earn = amount_deposited_in_earn(
        LCD_TEST, CHAIN_ID_TESTNET, WALLET_TEST.key.acc_address
    )

    assert amount_in_earn == EXPECTED_AMOUNT_IN_EARN
