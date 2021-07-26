import pathlib
import pprint

from terra_sdk.client import lcd

import anchorpy

if __name__ == "__main__":
    CHAIN_ID = "columbus-4"

    HERE = pathlib.Path(__file__).parent.resolve()
    ROOT = HERE.parent
    MNEM_PATH = ROOT / "mnemonic.txt"

    LCD = lcd.LCDClient(chain_id=CHAIN_ID, url=anchorpy.PUBLIC_NODE_URLS[CHAIN_ID])
    WALLET = LCD.wallet(anchorpy.mnem_key_from_file(MNEM_PATH))

    this_anc = anchorpy.Anchor(LCD, WALLET.key.acc_address)

    print(this_anc)
