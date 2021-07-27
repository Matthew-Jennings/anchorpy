from terra_sdk.core import coin, coins, Dec
from terra_sdk.key import mnemonic

CONTRACT_ADDRESSES = {
    "columbus-4": {
        "airdrop": "terra146ahqn6d3qgdvmj8cj96hh03dzmeedhsf0kxqm",
        "ANC": "terra14z56l0fp2lsf86zy3hty2z47ezkhnthtr9yq76",
        "aTerra": "terra1hzh9vpxhsk8253se0vv5jj6etdvxu3nv8z07zu",
        "bLunaHub": "terra1mtwph2juhj0rvjz7dy92gvl6xvukaxu8rfv8ts",
        "bLunaToken": "terra1kc87mu460fwkqte29rquh4hc20m54fxwtsx7gp",
        "bLunaReward": "terra17yap3mhph35pcwvhza38c2lkj7gzywzy05h7l0",
        "bLunaAirdrop": "terra199t7hg7w5vymehhg834r6799pju2q3a0ya7ae9",
        "collector": "terra14ku9pgw5ld90dexlyju02u4rn6frheexr5f96h",
        "community": "terra12wk8dey0kffwp27l5ucfumczlsc9aned8rqueg",
        "distributor": "terra1mxf7d5updqxfgvchd7lv6575ehhm8qfdttuqzz",
        "gov": "terra1f32xyep306hhcxxxf7mlyh0ucggc00rm2s9da5",
        "investor_vesting": "terra10evq9zxk2m86n3n3xnpw28jpqwp628c6dzuq42",
        "mmInterestModel": "terra1kq8zzq5hufas9t0kjsjc62t2kucfnx8txf547n",
        "mmOracle": "terra1cgg6yef7qcdm070qftghfulaxmllgmvk77nc7t",
        "mmMarket": "terra1sepfj7s0aeg5967uxnfk4thzlerrsktkpelm5s",
        "mmOverseer": "terra1tmnqgvg567ypvsvk6rwsga3srp7e3lg6u0elp8",
        "mmCustody": "terra1ptjp2vfjrwh0j0faj9r6katm640kgjxnwwq9kn",
        "mmLiquidation": "terra1w9ky73v4g7v98zzdqpqgf3kjmusnx4d4mvnac6",
        "mmDistributionModel": "terra14mufqpr5mevdfn92p4jchpkxp7xr46uyknqjwq",
        "staking": "terra1897an2xux840p9lrh6py3ryankc6mspw49xse3",
        "team_vesting": "terra1pm54pmw3ej0vfwn3gtn6cdmaqxt0x37e9jt0za",
        "terraswapblunaLunaPair": "terra1jxazgm67et0ce260kvrpfv50acuushpjsz2y0p",
        "terraswapblunaLunaLPToken": "terra1nuy34nwnsh53ygpc4xprlj263cztw7vc99leh2",
        "terraswapAncUstPair": "terra1gm5p3ner9x9xpwugn9sp6gvhd0lwrtkyrecdn3",
        "terraswapAncUstLPToken": "terra1gecs98vcuktyfkrve9czrpgtg0m3aq586x6gzm",
    },
    "tequila-0004": {
        "airdrop": "terra1u5ywhlve3wugzqslqvm8ks2j0nsvrqjx0mgxpk",
        "ANC": "terra1747mad58h0w4y589y3sk84r5efqdev9q4r02pc",
        "aTerra": "terra1ajt556dpzvjwl0kl5tzku3fc3p3knkg9mkv8jl",
        "bLunaHub": "terra1fflas6wv4snv8lsda9knvq2w0cyt493r8puh2e",
        "bLunaToken": "terra1u0t35drzyy0mujj8rkdyzhe264uls4ug3wdp3x",
        "bLunaReward": "terra1ac24j6pdxh53czqyrkr6ygphdeftg7u3958tl2",
        "bLunaAirdrop": "terra1334h20c9ewxguw9p9vdxzmr8994qj4qu77ux6q",
        "collector": "terra1hlctcrrhcl2azxzcsns467le876cfuzam6jty4",
        "community": "terra17g577z0pqt6tejhceh06y3lyeudfs3v90mzduy",
        "distributor": "terra1z7nxemcnm8kp7fs33cs7ge4wfuld307v80gypj",
        "gov": "terra16ckeuu7c6ggu52a8se005mg5c0kd2kmuun63cu",
        "investor_vesting": "not available in testnet",
        "mmInterestModel": "terra1m25aqupscdw2kw4tnq5ql6hexgr34mr76azh5x",
        "mmOracle": "terra1p4gg3p2ue6qy2qfuxtrmgv2ec3f4jmgqtazum8",
        "mmMarket": "terra15dwd5mj8v59wpj0wvt233mf5efdff808c5tkal",
        "mmOverseer": "terra1qljxd0y3j3gk97025qvl3lgq8ygup4gsksvaxv",
        "mmCustody": "terra1ltnkx0mv7lf2rca9f8w740ashu93ujughy4s7p",
        "mmLiquidation": "terra16vc4v9hhntswzkuunqhncs9yy30mqql3gxlqfe",
        "mmDistributionModel": "terra1u64cezah94sq3ye8y0ung28x3pxc37tv8fth7h",
        "staking": "terra19nxz35c8f7t3ghdxrxherym20tux8eccar0c3k",
        "team_vesting": "not available in testnet",
        "terraswapblunaLunaPair": "terra13e4jmcjnwrauvl2fnjdwex0exuzd8zrh5xk29v",
        "terraswapblunaLunaLPToken": "terra1tj4pavqjqjfm0wh73sh7yy9m4uq3m2cpmgva6n",
        "terraswapAncUstPair": "terra1wfvczps2865j0awnurk9m04u7wdmd6qv3fdnvz",
        "terraswapAncUstLPToken": "terra1vg0qyq92ky9z9dp0j9fv5rmr2s80sg605dah6f",
    },
}

PUBLIC_NODE_URLS = {
    "columbus-4": "https://lcd.terra.dev",
    "tequila-0004": "https://tequila-fcd.terra.dev",
}


class Anchor:
    def __init__(self, lcd, account_address):
        self.lcd = lcd
        self.account_address = account_address

    # Wallet

    @property
    def balance(self) -> coins.Coins:
        return self.lcd.bank.balance(address=self.account_address).to_dec_coins()

    # Anchor Earn

    @property
    def total_deposit_uaust(self) -> coin.Coin:
        result = self.lcd.wasm.contract_query(
            CONTRACT_ADDRESSES[self.lcd.chain_id]["aTerra"],
            {
                "balance": {
                    "address": self.account_address,
                },
            },
        )

        return coin.Coin("uaust", result["balance"])

    @property
    def total_deposit(self) -> coin.Coin:
        return uaust_to_uusd(self.lcd, self.total_deposit_uaust)

    # Anchor Borrow

    @property
    def total_collateral_ubluna(self) -> coin.Coin:
        amount = self.lcd.wasm.contract_query(
            CONTRACT_ADDRESSES[self.lcd.chain_id]["mmCustody"],
            {
                "borrower": {
                    "address": self.account_address,
                },
            },
        )["balance"]

        return coin.Coin("ubluna", Dec(amount))

    @property
    def total_collateral(self) -> coin.Coin:
        return ubluna_to_uusd(self.lcd, self.total_collateral_ubluna)

    @property
    def total_borrowed(self) -> coin.Coin:
        amount = self.lcd.wasm.contract_query(
            CONTRACT_ADDRESSES[self.lcd.chain_id]["mmMarket"],
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
            CONTRACT_ADDRESSES[self.lcd.chain_id]["mmMarket"],
            {
                "state": {},
            },
        )

        borrower_interest_idx = Dec(
            self.lcd.wasm.contract_query(
                CONTRACT_ADDRESSES[self.lcd.chain_id]["mmMarket"],
                {
                    "borrower_info": {"borrower": self.account_address},
                },
            )["interest_index"]
        )

        borrow_rate = Dec(
            self.lcd.wasm.contract_query(
                CONTRACT_ADDRESSES[self.lcd.chain_id]["mmInterestModel"],
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
    \t{coin_to_human_str(self.total_deposit_uaust)} ({coin_to_human_str(self.total_deposit)})

    Total collateral:
    \t{coin_to_human_str(self.total_collateral_ubluna)} ({coin_to_human_str(self.total_collateral)})

    Total owing:
    \t{coin_to_human_str(self.total_owing)}

    Loan to value ratio:
    \t{self.ltv:.2%}
"""


def mnem_key_from_file(mnem_fpath):
    with open(mnem_fpath) as f:
        this_mnem = f.readline()

    return mnemonic.MnemonicKey(mnemonic=this_mnem)


def uaust_to_uusd(lcd, offer_coin):

    if not offer_coin.denom == "uaust":
        raise ValueError("`offer_coin` denom must be 'uaust'")

    exchange_rate = lcd.wasm.contract_query(
        CONTRACT_ADDRESSES[lcd.chain_id]["mmMarket"], {"epoch_state": {}}
    )["exchange_rate"]

    return coin.Coin(denom="uusd", amount=int(offer_coin.mul(exchange_rate).amount))


def ubluna_to_uusd(lcd, offer_coin):

    if not offer_coin.denom == "ubluna":
        raise ValueError("`offer_coin` denom must be 'ubluna'")

    exchange_rate = lcd.wasm.contract_query(
        CONTRACT_ADDRESSES[lcd.chain_id]["mmOracle"],
        {
            "price": {
                "base": CONTRACT_ADDRESSES[lcd.chain_id]["bLunaToken"],
                "quote": "uusd",
            },
        },
    )["rate"]

    return coin.Coin(denom="uusd", amount=int(offer_coin.mul(exchange_rate).amount))


def coin_to_human_str(in_coin):
    DENOMS_TO_HUMAN = {
        "uusd": "UST",
        "uaust": "aUST",
        "uluna": "Luna",
        "ubluna": "bLuna",
    }

    return (
        f"{float(Dec(in_coin.amount).div(1e6)):,.4f} {DENOMS_TO_HUMAN[in_coin.denom]}"
    )
