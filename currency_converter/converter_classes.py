# -*- coding: utf-8 -*-
import os
import re
import locale

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from currency_converter.page_classes import FilterBlock
from currency_converter.page_classes import RadioGroup
from currency_converter.page_classes import Button


class WebUIHandler(object):
    def __init__(self, heading, url):

        self.driver = webdriver.Chrome(os.path.dirname(__file__) + '/chromedriver')

        self.url = url
        self.heading = heading

        self.driver.get(self.url)
        self.driver.fullscreen_window()

        try:
            element = WebDriverWait(self.driver, 10).until(
                ec.text_to_be_present_in_element((By.CSS_SELECTOR, '.header_widget'), text_=self.heading))

            self.Table = Table(self.driver)
            self.RadioGroup = RadioGroup(self.driver)
            self.FilterBlock = FilterBlock(self.driver)
            self.Button = Button(self.driver)
            self.ConverterResults = ConverterResults(self.driver)
        except Exception:
            self.driver.quit()
            raise Exception('Cannot initialize converter class!')

    def set_filter_block(self, curr_from, curr_to, amount):
        """
        :param curr_from: code of currency to sell
        :param curr_to: code of currency to buy
        :param amount: amount of money to sell (int or string)
        :return: None
        """
        self.FilterBlock.set_currency_to(curr_to)
        self.FilterBlock.set_currency_from(curr_from)
        self.FilterBlock.set_input_sum(amount)

    def set_radio_group(self, block, radio):
        """

        :param radio: name of radio button to check
        :param block: name of radio block
        :return: None
        """
        self.RadioGroup.set_checked(block, radio)

    def convert_data(self):
        """

        :return:
        """
        self.Button.push_button()

    @staticmethod
    def data_conversion(data):
        """

        :param data: list of digits with comma (in str type) to convert
        :return: list of digits with point
        """
        locale.setlocale(locale.LC_ALL, 'ru_RU')
        digits = [locale.atof(amnt.replace(' ', '')) for amnt in data]

        return digits

    def displayed_results(self):
        """
        :return: results of conversion displayed on the page
        """

        return self.ConverterResults.get_totals()

    def official_rates(self):
        """
        :return: dictionary of parsed table with official rates
        """

        return self.Table.parse_table()


class Table(object):
    def __init__(self, driver):

        self.driver = driver

    def get_rates_buy(self, table_head=None):
        """
        :param table_head: web element with <table> tag
                           optional value, can be passed if there are several tables on a page
        :return: header: name of the column
                 rates: list of rates to buy
        """

        if table_head:
            web_list = table_head.find_elements_by_css_selector('td[class*=cell_column_buy]')
        else:
            web_list = self.driver.find_elements_by_css_selector('td[class*=cell_column_buy]')

        try:
            header = web_list[0].text
            rates = [re.search('[1-9][\s|0-9]*,[0-9]{2}', el.text).group(0) for el in web_list[1:]]
        except AttributeError:
            self.driver.quit()
            raise AttributeError('Wrong rates format!')

        return header, rates

    def get_rates_sell(self, table_head=None):
        """

        :param table_head: web element with <table> tag
                           optional value, can be passed if there are several tables on a page
        :return: header: name of the column
                 rates: list of rates to sell
        """

        if table_head:
            web_list = table_head.find_elements_by_css_selector('td[class*=cell_column_sell]')
        else:
            web_list = self.driver.find_elements_by_css_selector('td[class*=cell_column_sell]')

        try:
            header = web_list[0].text
            rates = [re.search('[1-9][\s|0-9]*,[0-9]{2}', el.text).group(0) for el in web_list[1:]]
        except AttributeError:
            self.driver.quit()
            raise AttributeError('Wrong rates format!')

        return header, rates

    def get_ccy(self, table_head=None):
        """

        :param table_head: web element with <table> tag
                           optional value, can be passed if there are several tables on a page
        :return: header: name of the column
                 rates: list of currency names
        """

        if table_head:
            web_list = table_head.find_elements_by_css_selector('td[class*=cell_column_name]')
        else:
            web_list = self.driver.find_elements_by_css_selector('td[class*=cell_column_name]')

        header = web_list[0].text
        ccy = [re.findall('[A-Z]{3}', el.text) for el in web_list[1:]]

        return header, ccy

    def parse_table(self):
        """
        The function parses the header of table and
            the table body and put it in the dictionary
        :return: dictionary with grid data and name of columns as keys
        """

        grd_data = dict()

        table_root = self.driver.find_element_by_css_selector('table[class*=rates-current]')

        key_buy, rates_buy = self.get_rates_buy(table_head=table_root)
        key_sell, rates_sell = self.get_rates_sell(table_head=table_root)
        key_ccy, ccy = self.get_ccy(table_head=table_root)

        # get the array header
        grd_data[key_ccy] = ccy
        grd_data[key_buy] = WebUIHandler.data_conversion(rates_buy)
        grd_data[key_sell] = WebUIHandler.data_conversion(rates_sell)

        return grd_data


class ConverterResults(object):
    def __init__(self, driver):
        self.driver = driver

    def get_totals(self):
        """
        :return: dictionary with ccy name as a key and rate as value
        """
        try:
            results = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located(
                (By.CSS_SELECTOR, '.rates-converter-result__total')
            ))
        except Exception as error:
            self.driver.quit()
            raise Exception('Converter results are not displayed!')

        ccy = re.findall('[A-Z]{3}', results.text)
        amount_str = re.findall('\d[\s|0-9]*,[0-9]{2}', results.text)

        amount = WebUIHandler.data_conversion(amount_str)

        results = [(ccy_nme, amnt) for ccy_nme, amnt in zip(ccy, amount)]

        return dict(results)

