from terra_sdk.core import auth, coin, coins, Dec, wasm
from terra_sdk.key import mnemonic

from . import exchange, settings


class Anchor:
    def __init__(self, lcd, wallet):
        self.lcd = lcd
        self.wallet = wallet
        self.account_address = wallet.key.acc_address

    # Wallet

    @property
    def balance(self) -> coins.Coins:
        return self.lcd.bank.balance(address=self.account_address).to_dec_coins()

    # Anchor Earn

    @property
    def total_deposit_uaust(self) -> coin.Coin:
        result = self.lcd.wasm.contract_query(
            settings.CONTRACT_ADDRESSES[self.lcd.chain_id]["aTerra"],
            {
                "balance": {
                    "address": self.account_address,
                },
            },
        )

        return coin.Coin("uaust", result["balance"])

    @property
    def total_deposit(self) -> coin.Coin:
        return exchange.uaust_to_uusd(self.lcd, self.total_deposit_uaust)

    # Anchor Borrow

    @property
    def total_collateral_ubluna(self) -> coin.Coin:
        amount = self.lcd.wasm.contract_query(
            settings.CONTRACT_ADDRESSES[self.lcd.chain_id]["mmCustody"],
            {
                "borrower": {
                    "address": self.account_address,
                },
            },
        )["balance"]

        return coin.Coin("ubluna", Dec(amount))

    @property
    def total_collateral(self) -> coin.Coin:
        return exchange.ubluna_to_uusd(self.lcd, self.total_collateral_ubluna)

    @property
    def total_borrowed(self) -> coin.Coin:
        amount = self.lcd.wasm.contract_query(
            settings.CONTRACT_ADDRESSES[self.lcd.chain_id]["mmMarket"],
            {
                "borrower_info": {
                    "borrower": self.account_address,
                },
            },
        )["loan_amount"]

        return coin.Coin("uusd", amount)

    @property
    def total_owing(self) -> coin.Coin:
        market_state = self.lcd.wasm.contract_query(
            settings.CONTRACT_ADDRESSES[self.lcd.chain_id]["mmMarket"],
            {
                "state": {},
            },
        )

        borrower_interest_idx = Dec(
            self.lcd.wasm.contract_query(
                settings.CONTRACT_ADDRESSES[self.lcd.chain_id]["mmMarket"],
                {
                    "borrower_info": {"borrower": self.account_address},
                },
            )["interest_index"]
        )

        borrow_rate = Dec(
            self.lcd.wasm.contract_query(
                settings.CONTRACT_ADDRESSES[self.lcd.chain_id]["mmInterestModel"],
                {
                    "borrow_rate": {
                        "market_balance": "",
                        "total_reserves": "",
                        "total_liabilities": "",
                    },
                },
            )["rate"]
        )

        current_block_height = int(
            self.lcd.tendermint.block_info()["block"]["header"]["height"]
        )

        blocks_since_interest_last_accrued = (
            current_block_height - market_state["last_interest_updated"]
        )

        return self.total_borrowed.mul(
            Dec(market_state["global_interest_index"]).mul(
                borrow_rate.mul(blocks_since_interest_last_accrued).add(1)
            )
        ).div(borrower_interest_idx)

    @property
    def interest_charged(self) -> coin.Coin:
        return self.total_owing.sub(self.total_borrowed)

    @property
    def ltv(self) -> float:
        return float(
            self.total_owing.to_dec_coin().amount
            / self.total_collateral.to_dec_coin().amount
        )

    def __str__(self):

        balance_str = "\n".join(
            ["\t{}".format(coin_to_human_str(coin)) for coin in self.balance]
        )

        return f"""
Anchor details for address: {self.account_address}
    
    Bank balances:
    {balance_str}

    Total deposit:
    \t{coin_to_human_str(self.total_deposit)} ({coin_to_human_str(self.total_deposit_uaust)})

    Total collateral:
    \t{coin_to_human_str(self.total_collateral)} ({coin_to_human_str(self.total_collateral_ubluna)})

    Total owing:
    \t{coin_to_human_str(self.total_owing)}

    Loan to value ratio:
    \t{self.ltv:.2%}
"""


def mnem_key_from_file(mnem_fpath):
    with open(mnem_fpath) as f:
        this_mnem = f.readline()

    return mnemonic.MnemonicKey(mnemonic=this_mnem)


def coin_to_human_str(in_coin):
    DENOMS_TO_HUMAN = {
        "uusd": "UST",
        "uaust": "aUST",
        "uluna": "Luna",
        "ubluna": "bLuna",
        "uanc": "ANC",
    }

    return (
        f"{float(Dec(in_coin.amount).div(1e6)):,.4f} {DENOMS_TO_HUMAN[in_coin.denom]}"
    )
