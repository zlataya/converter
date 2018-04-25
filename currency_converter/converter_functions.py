
def calculate_rates(value_to_convert, rate_to_sell=1, rate_to_buy=1, ccy_to_sell=None, ccy_to_buy=None):
    """
    :param value_to_convert: initial amount of money to convert
    :param rate_to_sell: rate of currency to sell
    :param rate_to_buy: rate of currency to buy
    :param ccy_to_sell: code of currency to cell (for example, 'USD')
    :param ccy_to_buy: code of currency to buy (for example, 'RUB')
    :return: converted value rounded to 2 precision after the decimal point
    """

    # check if value_to_convert is integer or float
    if type(value_to_convert) not in (int, float):
        value_to_convert = float(value_to_convert)

    if not (ccy_to_sell and ccy_to_buy):
        ccy_to_sell = 'RUB'

    if ccy_to_buy == 'JPY':
        rate_to_sell = rate_to_sell / 100
    elif ccy_to_sell == 'JPY':
        rate_to_buy = rate_to_buy / 100

    if ccy_to_sell == 'RUB':
        converted_value = value_to_convert / rate_to_sell
    elif ccy_to_buy == 'RUB':
        converted_value = value_to_convert * rate_to_buy
    else:
        converted_value = value_to_convert * rate_to_buy / rate_to_sell

    return round(converted_value, 2)
