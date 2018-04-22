# -*- coding: utf-8 -*-
import pytest
from currency_converter.converter_functions import calculate_rates


def test_conversion_radios(converter, radio_buttons):

    # fill currency to buy, sell and amount of money
    converter.set_filter_block('RUB', 'USD', '100,999')

    # set all radio groups to default values
    for radio_group, radio in radio_buttons:
        converter.set_radio_group(radio_group, radio)

    # push the button
    converter.convert_data()

    # get official rates from the rates table on the page and calculate the rate
    calculated = converter.official_rates()
    expected_rate = calculate_rates(100.999, rate_to_sell=calculated['Продажа'][0],
                                    ccy_to_sell='RUB', ccy_to_buy='USD')

    # get the displayed result
    displayed = converter.displayed_results()

    # separated asserts used in order to get detailed results
    assert displayed['RUB'] == 100.99
    assert expected_rate == displayed['USD']
