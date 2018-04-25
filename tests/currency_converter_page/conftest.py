import pytest
import lxml.etree
from currency_converter.currency_converter_classes import ConverterPage


def pytest_report_header(config):
    return "Converter page testing..."


@pytest.fixture(scope='module')
def converter():
    rates_converter = ConverterPage(heading='Калькулятор иностранных валют',
                                    url='http://www.sberbank.ru/ru/quotes/converter')

    yield rates_converter

    rates_converter.driver.quit()


@pytest.fixture(scope='module')
def converter_parameters(request):

    def xml_tree(testing_part, tc_number):

        tree = lxml.etree.parse('%s_test_parameters.xml' % testing_part)
        test_cases = {elem.get('number'): elem for elem in tree.iter('test_case')}

        # save root for requested test case
        tc_root = test_cases[tc_number]

        filters = {el.tag: el.text for el in tc_root.iterchildren() if not el.getchildren()}

        groups_names = [el.attrib['name'] for el in tc_root.iterchildren() if el.getchildren()]

        # this depends on xml structure: now there is only one radio in xml so code takes only 1st element
        # but there can be all radios listed with parameters (for selected status) in xml
        # in this case it will be different realization
        radios = [el.getchildren()[0].text for el in tc_root.iterchildren()
                  if el.getchildren()]
        radio_groups = {group: radio for group, radio in zip(groups_names, radios)}

        return filters, radio_groups

    return xml_tree
