# -*- coding: utf-8 -*-
import pytest
from currency_converter.converter_functions import calculate_rates


@pytest.mark.parametrize('tc_num', ['1', '2', '3'])
def test_conversion_radios(converter, converter_parameters, tc_num):

    filters, radio_buttons = converter_parameters('radio', tc_num)

    # fill currency to buy, sell and amount of money
    converter.set_filter_block(filters['ccy_from'], filters['ccy_to'], filters['value'])

    # set all radio groups to default values
    for radio_group, radio in radio_buttons.items():
        converter.set_radio_group(radio_group, radio)

    # push the button
    converter.convert_data()

    # get official rates from the rates table on the page and calculate the rate
    calculated = converter.official_rates()
    expected_rate = calculate_rates(filters['value'], rate_to_sell=calculated['Продажа'][0],
                                    ccy_to_sell=filters['ccy_from'], ccy_to_buy=filters['ccy_to'])

    # get the displayed result
    displayed = converter.displayed_results()

    # separated asserts used in order to get detailed results
    assert displayed[filters['ccy_from']] == float(filters['value'])
    assert expected_rate == displayed[filters['ccy_to']]
