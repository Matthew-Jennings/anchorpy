import json

from terra_sdk.client import lcd

import anchorpy

if __name__ == "__main__":

    TX_HASH_TESTS = {
        "invalid type": (
            "71B74D813CFC48585CF758D01C73F49CBAA5864B9FB43715C9D464A73A1D0B0B"
        ),
        "invalid base64 msg": (
            "44A2D644D1F92F3D373107014C0DD50CC357BB63CFD2CB8F4E14D5B6647EC476"
        ),
        "invalid uint28 amount": (
            "44A2D644D1F92F3D373107014C0DD50CC357BB63CFD2CB8F4E14D5B6647EC476"
        ),
        "underflow": (
            "47B9FD82FC76CBC9CACC346658629262813EC5D33724A4338F509168EF168056"
        ),
        # "insufficient funds for fees": (
        #     "CDD975460DBE52D4153B81AFCB4EBDC914B6377796EEFC1BB252EA2B87257DEC"
        # ),
        "success": ("71B74D813CFC48585CF758D01C73F49CBAA5864B9FB43715C9D464A73A1D0B0B"),
    }
    CHAIN_ID = "tequila-0004"
    LCD = lcd.LCDClient(
        chain_id=CHAIN_ID, url=anchorpy.settings.PUBLIC_NODE_URLS[CHAIN_ID]
    )

    for k, tx_hash in TX_HASH_TESTS.items():
        print(f"\n{k}")
        print(
            json.dumps(
                LCD.tx.tx_info(tx_hash=tx_hash).to_data(), sort_keys=True, indent=2
            )
        )
