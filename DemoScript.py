from selenium import webdriver
import re
import unittest
from element_interaction import ElementInteraction
import time

__author__ = 'weyenk'


class Script(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome("/usr/bin/chromedriver")
        self.driver.maximize_window()
        self.driver.get("http://www.dice.com")
        self.ei = ElementInteraction(self.driver)

    def test_first(self):
        self.ei.is_page_ready()
        #self.ei.select_option("nav-search-dropdown", "9", "index", "searchDropdownBox")
        self.ei.enter_text("search-field-keyword", "python selenium")
        self.ei.click_object(".btn-primary")
        time.sleep(5)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()



