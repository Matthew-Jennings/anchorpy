import json
import logging
import pathlib

from terra_sdk.client import lcd
from terra_sdk.core import coin, coins, Dec

import anchorpy

log = logging.getLogger(__name__)

HERE = pathlib.Path(__file__).parent.resolve()
ROOT = HERE.parent

CHAIN_ID_TESTNET = "tequila-0004"
LCD_TEST = lcd.LCDClient(
    chain_id=CHAIN_ID_TESTNET, url=anchorpy.settings.PUBLIC_NODE_URLS[CHAIN_ID_TESTNET]
)
MNEM_TEST_PATH = ROOT / "mnemonic.txt"
WALLET_TEST = LCD_TEST.wallet(anchorpy.mnem_key_from_file(MNEM_TEST_PATH))


def test_anchor():
    anchor_test = anchorpy.Anchor(LCD_TEST, WALLET_TEST)

    BALANCE_EXPECTED = coins.Coins.from_str("3727582uluna,6489712uusd")
    assert anchor_test.balance == BALANCE_EXPECTED

    total_deposit_uaust_EXPECTED = coin.Coin("uaust", 1597783021)
    assert anchor_test.total_deposit_uaust == total_deposit_uaust_EXPECTED

    EARN_BALANCE_UUSD_EXPECTED = coin.Coin("uusd", 1718938303)
    assert anchor_test.total_deposit > EARN_BALANCE_UUSD_EXPECTED

    BORROW_COLLATERAL_BALANCE_EXPECTED = coin.Coin("ubluna", Dec(358245650))
    assert anchor_test.total_collateral_ubluna == BORROW_COLLATERAL_BALANCE_EXPECTED


def test_withdraw_from_earn():

    anchor_test = anchorpy.Anchor(LCD_TEST, WALLET_TEST)

    bank_balance_before = anchor_test.balance.get("uusd")
    total_deposit_before = anchor_test.total_deposit

    log.debug(
        "TXHASH: %s",
        anchor_test.withdraw_uusd_from_earn(coin.Coin("uusd", 1.365e9)).txhash,
    )

    bank_balance_after = anchor_test.balance.get("uusd")
    total_deposit_after = anchor_test.total_deposit

    total_removed_from_deposit = total_deposit_after.sub(total_deposit_before)
    total_added_to_bank = bank_balance_after.sub(bank_balance_before)

    implied_fees = total_removed_from_deposit.add(total_added_to_bank)
    implied_fee_percent = 100 * float(
        implied_fees.to_dec_coin().div(total_added_to_bank.to_dec_coin().amount).amount
    )

    log.debug(
        "Total removed from deposit: %s (%s)",
        total_removed_from_deposit,
        anchorpy.coin_to_human_str(total_removed_from_deposit),
    )

    log.debug(
        "Total added to bank: %s (%s)",
        total_added_to_bank,
        anchorpy.coin_to_human_str(total_added_to_bank),
    )
    log.debug(
        "Implied fees: %s (%s)", implied_fees, anchorpy.coin_to_human_str(implied_fees)
    )
    log.debug("Implied fee percent: %.3f%%", implied_fee_percent)


def test_deposit_from_earn():

    anchor_test = anchorpy.Anchor(LCD_TEST, WALLET_TEST)

    bank_balance_before = anchor_test.balance.get("uusd")
    total_deposit_before = anchor_test.total_deposit

    log.debug(
        json.dumps(
            eval(anchor_test.deposit_uusd_into_earn(coin.Coin("uusd", 5.4e9)).raw_log),
            sort_keys=True,
            indent=2,
        )
    )

    bank_balance_after = anchor_test.balance.get("uusd")
    total_deposit_after = anchor_test.total_deposit

    total_added_to_deposit = total_deposit_after.sub(total_deposit_before)
    total_removed_from_bank = bank_balance_after.sub(bank_balance_before)

    implied_fees = total_added_to_deposit.add(total_removed_from_bank)
    implied_fee_percent = 100 * float(
        implied_fees.to_dec_coin()
        .div(total_added_to_deposit.to_dec_coin().amount)
        .amount
    )

    log.debug(
        "Total added to deposit: %s (%s)",
        total_added_to_deposit,
        anchorpy.coin_to_human_str(total_added_to_deposit),
    )
    log.debug(
        "Total removed from bank: %s (%s)",
        total_removed_from_bank,
        anchorpy.coin_to_human_str(total_removed_from_bank),
    )
    log.debug(
        "Implied fees: %s (%s)", implied_fees, anchorpy.coin_to_human_str(implied_fees)
    )
    log.debug("Implied fee percent: %.3f%%", implied_fee_percent)


def test_ubluna_to_uusd():
    ubluna_coin_to_exchange = coin.Coin("ubluna", int(1e6))

    uusd_received = anchorpy.exchange.ubluna_to_uusd(LCD_TEST, ubluna_coin_to_exchange)

    log.debug(uusd_received)


def test_okay_to_use_int_for_uluna():
    """Flag if Luna price reaches high enough value that 1uLuna
    (1 micro Luna) is worth more than 0.01UST"""

    # swap_rate() returns int, so supply with 1e6 uluna (1 luna) for
    # better exchange rate precision
    uusd_coin_per_luna = LCD_TEST.market.swap_rate(coin.Coin("uluna", int(1e6)), "uusd")
    uusd_per_uluna = uusd_coin_per_luna.amount / 1e6
    uusd_cents_per_uluna = uusd_per_uluna * 100

    assert uusd_cents_per_uluna > 1
