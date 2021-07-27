from terra_sdk.core import coin, Dec

from . import settings


def uanc_to_uusd(lcd, offer_coin):

    if not offer_coin.denom == "uanc":
        raise ValueError("`offer_coin` denom must be 'uanc'")

    exchange_rate = Dec(
        lcd.wasm.contract_query(
            settings.CONTRACT_ADDRESSES[lcd.chain_id]["terraswapAncUstPair"],
            {
                "simulation": {
                    "offer_asset": {
                        "amount": str(int(1e6)),
                        "info": {
                            "token": {
                                "contract_addr": settings.CONTRACT_ADDRESSES[
                                    lcd.chain_id
                                ]["ANC"],
                            }
                        },
                    }
                }
            },
        )["return_amount"]
    ).div(1e6)

    return coin.Coin(denom="uusd", amount=int(offer_coin.mul(exchange_rate).amount))


def uaust_to_uusd(lcd, offer_coin):

    if not offer_coin.denom == "uaust":
        raise ValueError("`offer_coin` denom must be 'uaust'")

    exchange_rate = lcd.wasm.contract_query(
        settings.CONTRACT_ADDRESSES[lcd.chain_id]["mmMarket"], {"epoch_state": {}}
    )["exchange_rate"]

    return coin.Coin(denom="uusd", amount=int(offer_coin.mul(exchange_rate).amount))


def ubluna_to_uusd(lcd, offer_coin):

    if not offer_coin.denom == "ubluna":
        raise ValueError("`offer_coin` denom must be 'ubluna'")

    exchange_rate = lcd.wasm.contract_query(
        settings.CONTRACT_ADDRESSES[lcd.chain_id]["mmOracle"],
        {
            "price": {
                "base": settings.CONTRACT_ADDRESSES[lcd.chain_id]["bLunaToken"],
                "quote": "uusd",
            },
        },
    )["rate"]

    return coin.Coin(denom="uusd", amount=int(offer_coin.mul(exchange_rate).amount))
