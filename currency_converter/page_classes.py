import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class FilterBlock(object):
    def __init__(self, driver):
        self.driver = driver
        self.actionChains = ActionChains(self.driver)
        self.convert_to = self.driver.find_element_by_css_selector('div[class=rates-aside__filter-block-line] .select')

        self.convert_from = self.driver.find_element_by_css_selector('div[class*=converter-from] .select')

        self.input = self.driver.find_element_by_css_selector('input[placeholder="Сумма"]')

    def get_to_options(self):
        """
          This function gets all options from buy currency dropdown
        :return: dictionary with names of options as keys and web elements as values
        """
        to_options = dict([(el.get_attribute('innerHTML'), el)
                           for el in self.convert_to.find_elements_by_css_selector('div  > span')]
                          )
        return to_options

    def get_from_options(self):
        """
        This function gets all options from sell currency dropdown
        :return: dictionary with names of options as keys and web elements as values
        """
        from_options = dict([(el.get_attribute('innerHTML'), el)
                             for el in self.convert_from.find_elements_by_css_selector('div  > span')]
                            )
        return from_options

    @staticmethod
    def is_selected(el, value):
        """
        :param el: web element with current dropdown text
        :param value: value to check
        :return: True if the value is already selected otherwise False
        """
        return value == el.text.strip()

    def set_currency_to(self, value):
        """
        :param value: name of currency to chose
        :return: None
        """

        # move cursor to the element
        self.driver.execute_script("arguments[0].scrollIntoView();", self.convert_to)
        if self.is_selected(self.convert_to, value):
            return
        try:
            self.convert_to.click()
            self.get_to_options()[value].click()
        except Exception as w:
            self.driver.quit()
            raise Exception('Cannot locate option with value "%s" to set final currency: %s' % (value, w))

    def set_currency_from(self, value):
        """
        :param value: name of currency to chose
        :return: None
        """

        # move cursor to the element
        self.driver.execute_script("arguments[0].scrollIntoView();", self.convert_from)

        if self.is_selected(self.convert_from, value):
            return
        try:
            self.convert_from.click()
            self.get_from_options()[value].click()
        except Exception as w:
            self.driver.quit()
            raise Exception('Cannot locate option with value "%s" to set final currency: %s' % (value, w))

    @staticmethod
    def clear_input(el):
        """
        :param el: input web element to clean
        :return: None
        """
        # https://bugs.chromium.org/p/chromedriver/issues/detail?id=30
        # el.send_keys(Keys.COMMAND + 'a')

        # This was created since everything else are broken and does not work
        max_length = len(el.get_attribute('value'))
        for _ in range(max_length):
            el.send_keys(Keys.BACKSPACE)

    def set_input_sum(self, value):
        self.clear_input(self.input)
        self.input.send_keys(value)


class RadioGroup(object):
    def __init__(self, driver):
        self.driver = driver

        self.radios = dict()

        self.radio_groups = self.driver.find_elements_by_css_selector('div[class*=block_mode_converter]')
        self.titles = [el.text for el in self.driver.find_elements_by_css_selector('h6[class*=title-text]')]

        for title, block in zip(self.titles, self.radio_groups[:len(self.titles)]):
            self.radios[title] = block.find_elements_by_css_selector('label[class*=radio]')

    @staticmethod
    def is_checked(block, radio_text):
        """
        :param block: root web element for radio block
        :param radio_text: text of radio button
        :return: True if radio button with radio_text is already checked otherwise False
        """
        for radio in block:
            if radio.text == radio_text:
                return 'checked' in radio.get_attribute('class')

    @staticmethod
    def is_disabled(block, radio_text):
        """
        :param block: root web element for radio block
        :param radio_text: text of radio button
        :return: True if radio button with radio_text is disabled otherwise False
        """
        for radio in block:
            if radio.text == radio_text:
                return 'disabled' in radio.get_attribute('class')

    def set_checked(self, block, radio_text):
        """
          This function checks radio button according to radio_text
        :param block: root web element for radio block
        :param radio_text: text of radio button
        :return: None
        """
        # if block is specified find the radio elements for this block only
        current_block = self.radios[block]

        # if radio is already checked or disabled leave the function
        if self.is_checked(current_block, radio_text) or self.is_disabled(current_block, radio_text):
            return
        for radio in current_block:
            if radio.text == radio_text:
                # scroll to the radio button and click
                self.driver.execute_script("arguments[0].scrollIntoView(true);", radio)
                radio.click()
                break


class Button(object):
    def __init__(self, driver):
        self.driver = driver
        self.button = self.driver.find_element_by_css_selector('button[class=rates-button]')

    def push_button(self):
        # scroll to the button and click
        self.driver.execute_script("arguments[0].scrollIntoView();", self.button)
        self.button.click()

        # add this delay for refreshing result line
        time.sleep(0.5)
