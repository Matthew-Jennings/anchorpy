import json
import logging
import pathlib

import pytest
from terra_sdk.client import lcd
from terra_sdk.core import coin, coins, Dec

import anchorpy

log = logging.getLogger(__name__)


@pytest.fixture
def this_lcd():
    CHAIN_ID_TESTNET = "tequila-0004"
    return lcd.LCDClient(
        chain_id=CHAIN_ID_TESTNET,
        url=anchorpy.settings.PUBLIC_NODE_URLS[CHAIN_ID_TESTNET],
    )


@pytest.fixture
def this_wallet(this_lcd):
    HERE = pathlib.Path(__file__).parent.resolve()
    ROOT = HERE.parent

    MNEM_TEST_PATH = ROOT / "mnemonic.txt"
    return this_lcd.wallet(anchorpy.mnem_key_from_file(MNEM_TEST_PATH))


@pytest.fixture
def this_anchor(this_lcd, this_wallet):
    return anchorpy.Anchor(this_lcd, this_wallet)


@pytest.mark.skip(reason="Need to set up static Terra wallet first")
def test_anchor_getters(this_anchor):

    BALANCE_EXPECTED = coins.Coins.from_str("3727582uluna,6489712uusd")
    assert this_anchor.balance == BALANCE_EXPECTED

    total_deposit_uaust_EXPECTED = coin.Coin("uaust", 1597783021)
    assert this_anchor.total_deposit_uaust == total_deposit_uaust_EXPECTED

    EARN_BALANCE_UUSD_EXPECTED = coin.Coin("uusd", 1718938303)
    assert this_anchor.total_deposit > EARN_BALANCE_UUSD_EXPECTED

    BORROW_COLLATERAL_BALANCE_EXPECTED = coin.Coin("ubluna", Dec(358245650))
    assert this_anchor.total_collateral_ubluna == BORROW_COLLATERAL_BALANCE_EXPECTED


def test_withdraw_from_earn(this_anchor):

    bank_balance_before = this_anchor.balance.get("uusd")
    total_deposit_before = this_anchor.total_deposit

    log.debug(
        "TXHASH: %s",
        this_anchor.withdraw_uusd_from_earn(coin.Coin("uusd", 1.365e9)).txhash,
    )

    bank_balance_after = this_anchor.balance.get("uusd")
    total_deposit_after = this_anchor.total_deposit

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


def test_deposit_from_earn(this_anchor):

    bank_balance_before = this_anchor.balance.get("uusd")
    total_deposit_before = this_anchor.total_deposit

    log.debug(
        json.dumps(
            eval(this_anchor.deposit_uusd_into_earn(coin.Coin("uusd", 5.4e9)).raw_log),
            sort_keys=True,
            indent=2,
        )
    )

    bank_balance_after = this_anchor.balance.get("uusd")
    total_deposit_after = this_anchor.total_deposit

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


def test_ubluna_to_uusd(this_lcd):
    ubluna_coin_to_exchange = coin.Coin("ubluna", int(1e6))

    uusd_received = anchorpy.exchange.ubluna_to_uusd(this_lcd, ubluna_coin_to_exchange)

    log.debug(uusd_received)


def test_okay_to_use_int_for_uluna(this_lcd):
    """Flag if Luna price reaches high enough value that 1uLuna
    (1 micro Luna) is worth more than 0.01UST"""

    # swap_rate() returns int, so supply with 1e6 uluna (1 luna) for
    # better exchange rate precision
    uusd_coin_per_luna = this_lcd.market.swap_rate(coin.Coin("uluna", int(1e6)), "uusd")
    uusd_per_uluna = uusd_coin_per_luna.amount / 1e6
    uusd_cents_per_uluna = uusd_per_uluna * 100

    assert uusd_cents_per_uluna > 1
