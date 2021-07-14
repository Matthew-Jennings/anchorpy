import pathlib

from terra_sdk.client.lcd import LCDClient
from terra_sdk.core import Dec
from terra_sdk.core.coin import Coin

from terra_sdk.key.mnemonic import MnemonicKey

BALANCE_DIVISOR = 1e6
HERE = pathlib.Path(__file__).parent.resolve()
ROOT = HERE.parent.parent

CONTRACT_ADDRESSES = {
    "columbus-4": {
        "bLunaHub": "terra1mtwph2juhj0rvjz7dy92gvl6xvukaxu8rfv8ts",
        "bLunaToken": "terra1kc87mu460fwkqte29rquh4hc20m54fxwtsx7gp",
        "bLunaReward": "terra17yap3mhph35pcwvhza38c2lkj7gzywzy05h7l0",
        "bLunaAirdrop": "terra199t7hg7w5vymehhg834r6799pju2q3a0ya7ae9",
        "mmInterestModel": "terra1kq8zzq5hufas9t0kjsjc62t2kucfnx8txf547n",
        "mmOracle": "terra1cgg6yef7qcdm070qftghfulaxmllgmvk77nc7t",
        "mmMarket": "terra1sepfj7s0aeg5967uxnfk4thzlerrsktkpelm5s",
        "mmOverseer": "terra1tmnqgvg567ypvsvk6rwsga3srp7e3lg6u0elp8",
        "mmCustody": "terra1ptjp2vfjrwh0j0faj9r6katm640kgjxnwwq9kn",
        "mmLiquidation": "terra1w9ky73v4g7v98zzdqpqgf3kjmusnx4d4mvnac6",
        "mmDistributionModel": "terra14mufqpr5mevdfn92p4jchpkxp7xr46uyknqjwq",
        "aTerra": "terra1hzh9vpxhsk8253se0vv5jj6etdvxu3nv8z07zu",
        "terraswapblunaLunaPair": "terra1jxazgm67et0ce260kvrpfv50acuushpjsz2y0p",
        "terraswapblunaLunaLPToken": "terra1nuy34nwnsh53ygpc4xprlj263cztw7vc99leh2",
        "terraswapAncUstPair": "terra1gm5p3ner9x9xpwugn9sp6gvhd0lwrtkyrecdn3",
        "terraswapAncUstLPToken": "terra1gecs98vcuktyfkrve9czrpgtg0m3aq586x6gzm",
        "gov": "terra1f32xyep306hhcxxxf7mlyh0ucggc00rm2s9da5",
        "distributor": "terra1mxf7d5updqxfgvchd7lv6575ehhm8qfdttuqzz",
        "collector": "terra14ku9pgw5ld90dexlyju02u4rn6frheexr5f96h",
        "community": "terra12wk8dey0kffwp27l5ucfumczlsc9aned8rqueg",
        "staking": "terra1897an2xux840p9lrh6py3ryankc6mspw49xse3",
        "ANC": "terra14z56l0fp2lsf86zy3hty2z47ezkhnthtr9yq76",
        "airdrop": "terra146ahqn6d3qgdvmj8cj96hh03dzmeedhsf0kxqm",
        "team_vesting": "terra1pm54pmw3ej0vfwn3gtn6cdmaqxt0x37e9jt0za",
        "investor_vesting": "terra10evq9zxk2m86n3n3xnpw28jpqwp628c6dzuq42",
    },
    "tequila-0004": {
        "bLunaHub": "terra1fflas6wv4snv8lsda9knvq2w0cyt493r8puh2e",
        "bLunaToken": "terra1u0t35drzyy0mujj8rkdyzhe264uls4ug3wdp3x",
        "bLunaReward": "terra1ac24j6pdxh53czqyrkr6ygphdeftg7u3958tl2",
        "bLunaAirdrop": "terra1334h20c9ewxguw9p9vdxzmr8994qj4qu77ux6q",
        "mmInterestModel": "terra1m25aqupscdw2kw4tnq5ql6hexgr34mr76azh5x",
        "mmOracle": "terra1p4gg3p2ue6qy2qfuxtrmgv2ec3f4jmgqtazum8",
        "mmMarket": "terra15dwd5mj8v59wpj0wvt233mf5efdff808c5tkal",
        "mmOverseer": "terra1qljxd0y3j3gk97025qvl3lgq8ygup4gsksvaxv",
        "mmCustody": "terra1ltnkx0mv7lf2rca9f8w740ashu93ujughy4s7p",
        "mmLiquidation": "terra16vc4v9hhntswzkuunqhncs9yy30mqql3gxlqfe",
        "mmDistributionModel": "terra1u64cezah94sq3ye8y0ung28x3pxc37tv8fth7h",
        "aTerra": "terra1ajt556dpzvjwl0kl5tzku3fc3p3knkg9mkv8jl",
        "terraswapblunaLunaPair": "terra13e4jmcjnwrauvl2fnjdwex0exuzd8zrh5xk29v",
        "terraswapblunaLunaLPToken": "terra1tj4pavqjqjfm0wh73sh7yy9m4uq3m2cpmgva6n",
        "terraswapAncUstPair": "terra1wfvczps2865j0awnurk9m04u7wdmd6qv3fdnvz",
        "terraswapAncUstLPToken": "terra1vg0qyq92ky9z9dp0j9fv5rmr2s80sg605dah6f",
        "gov": "terra16ckeuu7c6ggu52a8se005mg5c0kd2kmuun63cu",
        "distributor": "terra1z7nxemcnm8kp7fs33cs7ge4wfuld307v80gypj",
        "collector": "terra1hlctcrrhcl2azxzcsns467le876cfuzam6jty4",
        "community": "terra17g577z0pqt6tejhceh06y3lyeudfs3v90mzduy",
        "staking": "terra19nxz35c8f7t3ghdxrxherym20tux8eccar0c3k",
        "ANC": "terra1747mad58h0w4y589y3sk84r5efqdev9q4r02pc",
        "airdrop": "terra1u5ywhlve3wugzqslqvm8ks2j0nsvrqjx0mgxpk",
        "investor_vesting": "not available in testnet",
        "team_vesting": "not available in testnet",
    },
}

PUBLIC_NODE_URLS = {
    "columbus-4": "https://lcd.terra.dev",
    "tequila-0004": "https://tequila-fcd.terra.dev",
}


def mnem_key_from_file(mnem_fpath):
    with open(mnem_fpath) as f:
        this_mnem = f.readline()

    return MnemonicKey(mnemonic=this_mnem)


def amount_deposited_in_earn(lcd, chain_id, account_address):
    result = lcd.wasm.contract_query(
        CONTRACT_ADDRESSES[chain_id]["aTerra"],
        {
            "balance": {
                "address": account_address,
            },
        },
    )

    return Coin("uusd", Dec(result["balance"])).div(BALANCE_DIVISOR)


def amount_deposited_in_borrow(lcd, chain_id, account_address):
    result = lcd.wasm.contract_query(
        CONTRACT_ADDRESSES[chain_id]["mmOverseer"],
        {
            "collaterals": {
                "borrower": account_address,
            },
        },
    )

    if result["collaterals"][0][0] == "terra1u0t35drzyy0mujj8rkdyzhe264uls4ug3wdp3x":
        denom = "ubluna"
    else:
        raise ValueError("Unsupported collateral token")

    return Coin(denom, Dec(result["collaterals"][0][1])).div(BALANCE_DIVISOR)


if __name__ == "__main__":
    chain_id = "tequila-0004"  # testnet (for now)
    lcd = LCDClient(chain_id=chain_id, url=PUBLIC_NODE_URLS[chain_id])

    aTerra_contract = CONTRACT_ADDRESSES[chain_id]["aTerra"]

    mnem_path = ROOT / "mnemonic.txt"
    mnem_key = mnem_key_from_file(mnem_path)

    wallet = lcd.wallet(mnem_key)

    balance = (
        lcd.bank.balance(address=wallet.key.acc_address)
        .to_dec_coins()
        .div(BALANCE_DIVISOR)
    )
    print(f"Balances (all denoms): {balance}")

    amount_in_earn = amount_deposited_in_earn(lcd, chain_id, wallet.key.acc_address)
    print(f"UST deposited in earn: {amount_in_earn}")

    total_collateral_in_borrow = amount_deposited_in_borrow(
        lcd, chain_id, wallet.key.acc_address
    )
    print(f"bLuna deposited in borrow: {total_collateral_in_borrow}")

    total_collateral_in_borrow_equiv_luna = Coin(
        denom="uluna", amount=int(total_collateral_in_borrow.amount * BALANCE_DIVISOR)
    )
    print(
        f"bLuna deposited in borrow in equiv microLuna: {total_collateral_in_borrow_equiv_luna}"
    )  # Assume 1:1 price for Luna / bLuna

    total_collateral_in_borrow_equiv_ust = (
        lcd.market.swap_rate(total_collateral_in_borrow_equiv_luna, "uusd")
        .to_dec_coin()
        .div(BALANCE_DIVISOR)
    )

    # This gives a value appriox 0.5% lower than value quoted on WebApp. Appears to be due to
    # lower price of Luna quoted by lcd.market.,swap_rate() than price of bLuna quoted in
    # https://app.anchorprotocol.com/borrow
    #
    # Use Terraswap instead? Unclear how Anchor calculatres price of bLuna..
    #
    # The 1:1 Luna/bLuna price assumption appears NOT to be the cause of this discrepancy, since:
    # - Anchor's burn module quotes a price difference of 0.0007% (essentially equal)
    # - Anchor's INSTANT burn module quotes a 1.52% price difference (3 × observed differeence)
    # - Terraswap bLuna/Luna price matches Anchor's instant burn

    print(
        f"bLuna deposited in borrow in equiv UST: {total_collateral_in_borrow_equiv_ust}"
    )

    # TODO: debug or adopt approach in https://github.com/jonnyli1125/terraswap-monitor/blob/main/terraswap.py ?

    # Is 0.5% good enough for managing liquidations? Want confidence that this is an unchanging discrepancy...
