from anchorpy import anchor
from terra_sdk.client import lcd
from terra_sdk.core import coin, coins, Dec

import anchorpy

if __name__ == "__main__":

    print(f"UUSD gas price:\n\t{anchorpy.settings.GAS_PRICES}")
