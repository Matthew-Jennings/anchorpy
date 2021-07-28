import base64

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

    def withdraw_uusd_from_earn(
        self, withdraw_amount_uusd: coin.Coin, add_buffer: bool = True
    ) -> coin.Coin:

        BUFFER_MULTIPLIER = 1.0001  # is this enough?

        if add_buffer:
            withdraw_amount_uusd = withdraw_amount_uusd.mul(BUFFER_MULTIPLIER)

        fee_estimate = self._estimate_withdraw_fee(withdraw_amount_uusd)

        tax_estimate = self.stability_fee(withdraw_amount_uusd)
        print(f"\nStability fee: {tax_estimate}")

        withdraw_amount_uusd_with_fees = withdraw_amount_uusd.add(
            fee_estimate.amount.get("uusd")
        ).add(tax_estimate)

        withdraw_amount_aust_with_fees = exchange.uusd_to_uaust(
            self.lcd, withdraw_amount_uusd_with_fees
        )

        exec_msg = (
            wasm.MsgExecuteContract(
                sender=self.account_address,
                contract=settings.CONTRACT_ADDRESSES[self.lcd.chain_id]["aTerra"],
                execute_msg={
                    "send": {
                        "contract": settings.CONTRACT_ADDRESSES[self.lcd.chain_id][
                            "mmMarket"
                        ],
                        "amount": str(int(withdraw_amount_aust_with_fees.amount)),
                        "msg": encode_hook_msg("redeem_stable"),
                    }
                },
            ),
        )

        send_tx = self.wallet.create_and_sign_tx(
            exec_msg,
            fee=fee_estimate,
        )

        return self.lcd.tx.broadcast(send_tx)

    def _estimate_withdraw_fee(self, withdraw_amount_uusd):

        withdraw_amount_aust = exchange.uusd_to_uaust(self.lcd, withdraw_amount_uusd)

        exec_msg_nofee = (
            wasm.MsgExecuteContract(
                sender=self.account_address,
                contract=settings.CONTRACT_ADDRESSES[self.lcd.chain_id]["aTerra"],
                execute_msg={
                    "send": {
                        "contract": settings.CONTRACT_ADDRESSES[self.lcd.chain_id][
                            "mmMarket"
                        ],
                        "amount": str(int(withdraw_amount_aust.amount)),
                        "msg": encode_hook_msg("redeem_stable"),
                    }
                },
            ),
        )
        send_tx_nofee = self.wallet.create_tx(exec_msg_nofee)

        return self.lcd.tx.estimate_fee(
            tx=send_tx_nofee,
            gas_prices=settings.GAS_PRICES,
            gas_adjustment=1.05,
            fee_denoms=["uusd"],
        )

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

    def stability_fee(self, amount_coin):

        tax_cap = self.lcd.treasury.tax_cap(amount_coin.denom)

        tax_rate = self.lcd.treasury.tax_rate()
        # Add 1 uusd to tax_uncapped to compensate for later
        # flooring performed by to_int_coin()
        tax_uncapped = amount_coin.mul(tax_rate).add(coin.Coin(amount_coin.denom, 1))

        return min(tax_cap, tax_uncapped)

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
        "ukrw": "KRT",
        "usdr": "SDT",
        "uanc": "ANC",
    }

    return (
        f"{float(Dec(in_coin.amount).div(1e6)):,.4f} {DENOMS_TO_HUMAN[in_coin.denom]}"
    )


def encode_hook_msg(key_str_to_encode):

    # MUST have double quotes enclosing `key_str_to_encode`
    msg_to_encode = f'{{"{key_str_to_encode}":{{}}}}'

    return base64.b64encode(bytes(msg_to_encode, "utf-8")).decode("utf-8")
