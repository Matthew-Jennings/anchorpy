from terra_sdk.client import lcd
from terra_sdk.core import coin

import anchorpy
from anchorpy import exchange

if __name__ == "__main__":
    CHAIN_ID = "tequila-0004"
    # CHAIN_ID = "columbus-4"
    LCD = lcd.LCDClient(
        chain_id=CHAIN_ID, url=anchorpy.settings.PUBLIC_NODE_URLS[CHAIN_ID]
    )

    print(
        f"1 aUST = {anchorpy.coin_to_human_str(exchange.uaust_to_uusd(LCD, coin.Coin('uaust', 1e6)), decimals=8)}"
    )
    print(
        f"1 bLuna = {anchorpy.coin_to_human_str(exchange.ubluna_to_uusd(LCD, coin.Coin('ubluna', 1e6)), decimals=8)}"
    )
    print(
        f"1 ANC = {anchorpy.coin_to_human_str(exchange.uanc_to_uusd(LCD, coin.Coin('uanc', 1e6)), decimals=8)}"
    )
