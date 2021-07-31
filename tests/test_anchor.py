import logging
import math
import os
import pathlib

import pytest
from terra_sdk.client import lcd
from terra_sdk.core import coin, coins, Dec

import anchorpy

log = logging.getLogger(__name__)

CHAIN_ID_TESTNET = "tequila-0004"

reason_no_test_wallet = "Awaiting setup of a suitable test wallet"
is_in_github_actions = os.getenv("GITHUB_ACTIONS", "False").lower() in ("true", "1")


@pytest.fixture
def this_lcd():
    return lcd.LCDClient(
        chain_id=CHAIN_ID_TESTNET,
        url=anchorpy.settings.PUBLIC_NODE_URLS[CHAIN_ID_TESTNET],
    )


@pytest.fixture
def this_wallet(this_lcd):
    if is_in_github_actions:
        pytest.skip(reason=reason_no_test_wallet)

    HERE = pathlib.Path(__file__).parent.resolve()
    ROOT = HERE.parent

    MNEM_TEST_PATH = ROOT / "mnemonic.txt"
    return this_lcd.wallet(anchorpy.mnem_key_from_file(MNEM_TEST_PATH))


@pytest.fixture
def this_anc(this_lcd, this_wallet):
    if is_in_github_actions:
        pytest.skip(reason=reason_no_test_wallet)
    return anchorpy.Anchor(this_lcd, this_wallet)


@pytest.mark.skip(reason=reason_no_test_wallet)
def test_anchor_getters(this_anc):

    BALANCE_EXPECTED = coins.Coins.from_str("3727582uluna,6489712uusd")
    assert this_anc.balance == BALANCE_EXPECTED

    total_deposit_uaust_EXPECTED = coin.Coin("uaust", 1597783021)
    assert this_anc.total_deposit_uaust == total_deposit_uaust_EXPECTED

    EARN_BALANCE_UUSD_EXPECTED = coin.Coin("uusd", 1718938303)
    assert this_anc.total_deposit > EARN_BALANCE_UUSD_EXPECTED

    BORROW_COLLATERAL_BALANCE_EXPECTED = coin.Coin("ubluna", Dec(358245650))
    assert this_anc.total_collateral_ubluna == BORROW_COLLATERAL_BALANCE_EXPECTED


@pytest.mark.skipif(is_in_github_actions, reason=reason_no_test_wallet)
def test_withdraw_from_earn(this_anc):

    WITHDRAW_AMOUNT = coin.Coin("uusd", 1)

    block_height_before = this_anc.block_height
    bank_balance_before = this_anc.balance.get("uusd")
    total_deposit_before = this_anc.total_deposit

    result = this_anc.withdraw_uusd_from_earn(WITHDRAW_AMOUNT, receive_full_amount=True)
    log.debug("TXHASH: %s", result.txhash)

    bank_balance_after = this_anc.balance.get("uusd")
    total_deposit_after = this_anc.total_deposit
    max_blocks_since_withdrawal_initiated = this_anc.block_height - block_height_before

    # Withdraw amount is denominated in uaUST. This amount appreciates
    # in value during the time between query msg construction and
    # contract execution.
    appreciation_adjustment = WITHDRAW_AMOUNT.mul(
        this_anc.deposit_rate_per_block_at_last_epoch.mul(
            max_blocks_since_withdrawal_initiated
        )
    )

    total_removed_from_deposit = total_deposit_after.sub(total_deposit_before)
    anchorpy.log_human_coin("Total removed from deposit", total_removed_from_deposit)

    total_added_to_bank = bank_balance_after.sub(bank_balance_before)
    anchorpy.log_human_coin("Total added to bank", total_added_to_bank)

    implied_fees = total_removed_from_deposit.add(total_added_to_bank)
    anchorpy.log_human_coin("Implied fees", implied_fees)

    if implied_fees.amount > 0:
        implied_fee_percent = 100 * float(
            implied_fees.div(total_added_to_bank.to_dec_coin().amount).amount
        )
        log.debug("Implied fee percent: %.3f%%", implied_fee_percent)

    # Should receive no less than WITHDRAW_AMOUNT in bank
    assert total_added_to_bank >= WITHDRAW_AMOUNT

    # Actual received amount permitted to be greater than requested, but
    # by no more than the calculated aUST adjustment (otherwise there's
    # some other cause for increased actual withdrawal amount)
    assert math.isclose(
        total_added_to_bank.amount,
        WITHDRAW_AMOUNT.amount,
        abs_tol=appreciation_adjustment.amount,
    )


@pytest.mark.skipif(is_in_github_actions, reason=reason_no_test_wallet)
def test_deposit_from_earn(this_anc):

    DEPOSIT_AMOUNT = coin.Coin("uusd", 2e9)

    block_height_before = this_anc.block_height
    bank_balance_before = this_anc.balance.get("uusd")
    total_deposit_before = this_anc.total_deposit

    result = this_anc.deposit_uusd_into_earn(DEPOSIT_AMOUNT)
    log.debug("TXHASH: %s", result.txhash)

    bank_balance_after = this_anc.balance.get("uusd")
    total_deposit_after = this_anc.total_deposit
    max_blocks_since_deposit_initiated = this_anc.block_height - block_height_before

    # Total deposit is natively denominated in uaUST, which appreciates
    # in value during the time between querying the deposit balance
    # prior to making an additional deposit and querying the deposit
    # balance afgter the deposit is completed. Note that this slightly
    # differs from the related effect observed for withdrawals, as here
    # the relevant value appreciation is that of the deposit balance,
    # not the amount to deposit.
    appreciation_adjustment = total_deposit_after.mul(
        this_anc.deposit_rate_per_block_at_last_epoch.mul(
            max_blocks_since_deposit_initiated
        )
    )
    log.debug(
        "Max increase in deposit value due to aUST appreciation: %s",
        appreciation_adjustment,
    )

    total_added_to_deposit = total_deposit_after.sub(total_deposit_before)
    anchorpy.log_human_coin("Total added to deposit", total_added_to_deposit)

    total_removed_from_bank = bank_balance_after.sub(bank_balance_before)
    anchorpy.log_human_coin("Total removed from bank", total_removed_from_bank)

    implied_fees = total_added_to_deposit.add(total_removed_from_bank)
    anchorpy.log_human_coin("Implied fees", implied_fees)

    if implied_fees.amount > 0:
        implied_fee_percent = 100 * float(
            implied_fees.div(total_added_to_deposit.to_dec_coin().amount).amount
        )
        log.debug("Implied fee percent: %.3f%%", implied_fee_percent)

    assert total_added_to_deposit >= DEPOSIT_AMOUNT
    assert math.isclose(
        total_added_to_deposit.amount,
        DEPOSIT_AMOUNT.amount,
        abs_tol=appreciation_adjustment.amount,
    )


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
