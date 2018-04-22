import csv
import pytest
import xml.etree.ElementTree as ET
from currency_converter.converter_classes import ConverterPage


def pytest_report_header(config):
    return "Rates converter page testing..."


@pytest.fixture(scope='module')
def converter():
    rates_converter = ConverterPage(heading='Калькулятор иностранных валют',
                                    url='http://www.sberbank.ru/ru/quotes/converter')

    yield rates_converter

    rates_converter.driver.quit()


def test_generate_tests(metafunc):
    with open('converter_radio_button_params.csv', 'r') as cf:
        csv_reader = dict(csv.DictReader(cf))
    if 'radio_buttons' in metafunc.fixturenames:
        metafunc.parametrize('radio_buttons', csv_reader, indirect=True, scope="module")


@pytest.fixture(scope='module')
def radio_buttons(request):
    return request