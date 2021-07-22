import pathlib

from terra_sdk.client import lcd
from terra_sdk.core import coin, coins, Dec

from anchorman import anchor

HERE = pathlib.Path(__file__).parent.resolve()
ROOT = HERE.parent

CHAIN_ID_TESTNET = "tequila-0004"
LCD_TEST = lcd.LCDClient(
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
    assert anchor_test.borrow_collateral_balance == BORROW_COLLATERAL_BALANCE_EXPECTED


def test_okay_to_use_int_for_uluna():
    """Flag if Luna price reaches high enough value that 1uLuna
    (1 micro Luna) is worth more than 0.01UST"""

    # swap_rate() returns int, so supply with 1e6 uluna (1 luna) for
    # better exchange rate precision
    uusd_coin_per_luna = LCD_TEST.market.swap_rate(coin.Coin("uluna", int(1e6)), "uusd")
    uusd_per_uluna = uusd_coin_per_luna.amount / 1e6
    uusd_cents_per_uluna = uusd_per_uluna * 100

    assert uusd_cents_per_uluna > 1
