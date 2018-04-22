# -*- coding: utf-8 -*-
import pytest
from currency_converter.converter_functions import calculate_rates

radio_default_values = [('Источник', 'Счет в Сбербанке'),
                        ('Получение', 'Безналичная оплата услуг/товаров'),
                        ('Способ обмена', 'Банкомат / УС'),
                        ('Пакет услуг', 'Нет пакета'),
                        ('Время', 'Текущее')]

ccy_names = ['JPY', 'CHF', 'EUR', 'GBP', 'USD']


@pytest.mark.parametrize('ccy_to', ccy_names)
def test_conversion_from_rub(converter, ccy_to):

    # fill currency to buy, sell and amount of money
    converter.set_filter_block('RUB', ccy_to, '999999999999,999')

    # set all radio groups to default values
    for radio_group, radio in radio_default_values:
        converter.set_radio_group(radio_group, radio)

    # push the button
    converter.convert_data()

    # get official rates from the rates table on the page and calculate the rate
    calculated = converter.official_rates()
    expected_rate = calculate_rates(999999999999.99, rate_to_sell=calculated['Продажа'][0],
                                    ccy_to_sell='RUB', ccy_to_buy=ccy_to)

    # get the displayed result
    displayed = converter.displayed_results()

    # separated asserts used in order to get detailed results
    assert displayed['RUB'] == 999999999999.99
    assert expected_rate == displayed[ccy_to]


@pytest.mark.parametrize('ccy_from', ccy_names)
def test_conversion_to_rub(converter, ccy_from):

    # fill currency to buy, sell and amount of money
    converter.set_filter_block(ccy_from, 'RUB', 1)

    # set all radio groups to default values
    for radio_group, radio in radio_default_values:
        converter.set_radio_group(radio_group, radio)

    # push the button
    converter.convert_data()

    # get official rates from the rates table on the page and calculate the rate
    calculated = converter.official_rates()
    expected_rate = calculate_rates(1.0, rate_to_buy=calculated['Покупка'][0],
                                    ccy_to_buy='RUB', ccy_to_sell=ccy_from)

    # get the displayed result
    displayed = converter.displayed_results()

    # separated asserts used in order to get detailed results
    assert displayed[ccy_from] == 1.00
    assert expected_rate == displayed['RUB']


@pytest.mark.parametrize('ccy_from, ccy_to', [(frm, to) for frm in ccy_names for to in ccy_names if frm != to])
def test_conversion_from_to(converter, ccy_from, ccy_to):

    # fill currency to buy, sell and amount of money
    converter.set_filter_block(ccy_from, ccy_to, 1000)

    # set all radio groups to default values
    for radio_group, radio in radio_default_values:
        converter.set_radio_group(radio_group, radio)

    # push the button
    converter.convert_data()

    # get official rates from the rates table on the page and calculate the rate
    calculated = converter.official_rates()
    expected_rate = calculate_rates(1000, rate_to_sell=calculated['Продажа'][1], rate_to_buy=calculated['Покупка'][0],
                                    ccy_to_buy=ccy_to, ccy_to_sell=ccy_from)

    # get the displayed result
    displayed = converter.displayed_results()

    # separated asserts used in order to get detailed results
    assert displayed[ccy_from] == 1000.00
    assert expected_rate == displayed[ccy_to]
