import pathlib

from terra_sdk.client import lcd
from terra_sdk.core import coin, coins, Dec

import anchorpy

if __name__ == "__main__":
    CHAIN_ID = "columbus-4"
    LCD = lcd.LCDClient(chain_id=CHAIN_ID, url=anchorpy.PUBLIC_NODE_URLS[CHAIN_ID])

    print(
        f"1 aUST = {anchorpy.coin_to_human_str(anchorpy.uaust_to_uusd(LCD, coin.Coin('uaust', 1e6)))}"
    )
    print(
        f"1 bLuna = {anchorpy.coin_to_human_str(anchorpy.ubluna_to_uusd(LCD, coin.Coin('ubluna', 1e6)))}"
    )
    print(
        f"1 ANC = {anchorpy.coin_to_human_str(anchorpy.uanc_to_uusd(LCD, coin.Coin('uanc', 1e6)))}"
        # anchorpy.uanc_to_uusd(LCD, coin.Coin("uanc", 1e6))
    )
