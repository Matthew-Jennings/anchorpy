import pathlib

from terra_sdk.client.lcd import LCDClient
from terra_sdk.core import Dec
from terra_sdk.core import coin

from anchorman import anchor

HERE = pathlib.Path(__file__).parent.resolve()
ROOT = HERE.parent

CHAIN_ID_TESTNET = "tequila-0004"
LCD_TEST = LCDClient(
    chain_id=CHAIN_ID_TESTNET, url=anchor.PUBLIC_NODE_URLS[CHAIN_ID_TESTNET]
)
MNEM_PATH_TEST = ROOT / "mnemonic.txt"
WALLET_TEST = LCD_TEST.wallet(anchor.mnem_key_from_file(MNEM_PATH_TEST))


def test_anchor():
    """[summary]"""

    anchor_test = anchor.Anchor(LCD_TEST, WALLET_TEST.key.acc_address)

    # BALANCE_EXPECTED =
    print(anchor_test.balance)
    print(type(anchor_test.balance))

    print(anchor_test.earn_balance)
    EARN_BALANCE_EXPECTED = coin.Coin("uusd", Dec(1597783021))
    assert anchor_test.earn_balance == EARN_BALANCE_EXPECTED

    print(anchor_test.borrow_collateral_balance)
    BORROW_COLLATERAL_BALANCE_EXPECTED = coin.Coin("ubluna", Dec(358245650))
    assert BORROW_COLLATERAL_BALANCE_EXPECTED == anchor_test.borrow_collateral_balance
