from terra_sdk.core import coin, Dec

from anchorpy import exchange


def test_round_to_int_coin():
    DOWNROUNDED_COIN_EXPECTED = coin.Coin("uusd", 1)
    assert DOWNROUNDED_COIN_EXPECTED.is_int_coin()

    dec_coin_to_round_down = coin.Coin("uusd", 1.49)
    assert dec_coin_to_round_down.is_dec_coin()
    assert dec_coin_to_round_down.amount == Dec(1.49)

    dec_coin_rounded_down = exchange.round_to_int_coin(dec_coin_to_round_down)
    assert dec_coin_rounded_down.is_int_coin()
    assert dec_coin_rounded_down == DOWNROUNDED_COIN_EXPECTED

    UPROUNDED_COIN_EXPECTED = coin.Coin("uusd", 2)
    assert UPROUNDED_COIN_EXPECTED.is_int_coin()

    dec_coin_to_round_up = coin.Coin("uusd", 1.51)
    assert dec_coin_to_round_up.is_dec_coin()
    assert dec_coin_to_round_up.amount == Dec(1.51)

    dec_coin_rounded_up = exchange.round_to_int_coin(dec_coin_to_round_up)
    assert dec_coin_rounded_up.is_int_coin()
    assert dec_coin_rounded_up == UPROUNDED_COIN_EXPECTED


def test_ceil_to_int_coin():
    CEILED_COIN_EXPECTED = coin.Coin("uusd", 2)
    assert CEILED_COIN_EXPECTED.is_int_coin()

    dec_coin_to_round_down = coin.Coin("uusd", 1.49)
    assert dec_coin_to_round_down.is_dec_coin()
    assert dec_coin_to_round_down.amount == Dec(1.49)

    dec_coin_rounded_down = exchange.ceil_to_int_coin(dec_coin_to_round_down)
    assert dec_coin_rounded_down.is_int_coin()
    assert dec_coin_rounded_down == CEILED_COIN_EXPECTED

    dec_coin_to_round_up = coin.Coin("uusd", 1.51)
    assert dec_coin_to_round_up.is_dec_coin()
    assert dec_coin_to_round_up.amount == Dec(1.51)

    dec_coin_rounded_up = exchange.ceil_to_int_coin(dec_coin_to_round_up)
    assert dec_coin_rounded_up.is_int_coin()
    assert dec_coin_rounded_up == CEILED_COIN_EXPECTED


if __name__ == "__main__":
    test_round_to_int_coin()
