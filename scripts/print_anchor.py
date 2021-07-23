import inspect
import pathlib
import pprint

from terra_sdk.client import lcd

from anchorman import anchor

if __name__ == "__main__":
    CHAIN_ID = "tequila-0004"

    HERE = pathlib.Path(__file__).parent.resolve()
    ROOT = HERE.parent
    MNEM_PATH = ROOT / "mnemonic.txt"

    LCD = lcd.LCDClient(chain_id=CHAIN_ID, url=anchor.PUBLIC_NODE_URLS[CHAIN_ID])
    WALLET = LCD.wallet(anchor.mnem_key_from_file(MNEM_PATH))

    this_anc = anchor.Anchor(LCD, WALLET.key.acc_address)

    dump = [
        member
        for member in inspect.getmembers(this_anc)
        if not member[0].startswith("_")
    ]

    pprint.pprint(dump)
