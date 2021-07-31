import logging

from terra_sdk.core import Dec

log = logging.getLogger(__name__)


def coin_to_human_str(in_coin, decimals=4):
    DENOMS_TO_HUMAN = {
        "uusd": "UST",
        "uaust": "aUST",
        "uluna": "Luna",
        "ubluna": "bLuna",
        "ukrw": "KRT",
        "usdr": "SDT",
        "uanc": "ANC",
    }

    return (
        f"{float(Dec(in_coin.amount).div(1e6)):,.{decimals}f} "
        f"{DENOMS_TO_HUMAN[in_coin.denom]}"
    )


def log_human_coin(label, coin_to_log, level_str="debug"):

    level_str = level_str.lower()

    level_dict = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    log.log(
        level_dict[level_str],
        "%s: %s (%s)",
        label,
        coin_to_log,
        coin_to_human_str(coin_to_log),
    )
