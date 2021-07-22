import pathlib

from terra_sdk.client.lcd import LCDClient
from terra_sdk.core import Dec
from terra_sdk.core import coin, coins

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
    anchor_test = anchor.Anchor(LCD_TEST, WALLET_TEST.key.acc_address)

    BALANCE_EXPECTED = coins.Coins.from_str("3727582uluna,6489712uusd")
    assert anchor_test.balance == BALANCE_EXPECTED

    EARN_BALANCE_UAUST_EXPECTED = coin.Coin("uaust", 1597783021)
    assert anchor_test.earn_balance_uaust == EARN_BALANCE_UAUST_EXPECTED

    EARN_BALANCE_UUSD_EXPECTED = coin.Coin("uusd", 1718938303)
    assert anchor_test.earn_balance_uusd > EARN_BALANCE_UUSD_EXPECTED

    BORROW_COLLATERAL_BALANCE_EXPECTED = coin.Coin("ubluna", Dec(358245650))
    assert BORROW_COLLATERAL_BALANCE_EXPECTED == anchor_test.borrow_collateral_balance
