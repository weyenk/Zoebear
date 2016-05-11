from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.selenium import selenium
import re
from element_identification import ElementIdentification
import pickle
from selenium.webdriver.common.alert import Alert
import time
from selenium.webdriver.common.action_chains import ActionChains

class ElementInteraction(ElementIdentification):

    def __init__(self, driver):
        self.driver = driver
        self.ei = ElementIdentification(self.driver)

    def __soft_assert_page_changed(self, preclick, postclick):
        pickled_preclick = pickle.dumps(preclick)
        pickled_postclick = pickle.dumps(postclick)
        if pickled_preclick == pickled_postclick:
            return True
        else:
            return False

    def __error_check(self):
        # Determine if page contains any common errors
        # Check config for custom errors
        pass

    def __post_back_check(self, element):
        match = re.search("(P|p)ost(\s|_)*(B|b)ack", element.get_attribute('outerHTML'))
        if match:
            return True
        else:
            return False

    def __wait_for_post_back_to_complete(self, element):
        ''' It may be wise to allow the timeout to be passed from the json file.
            For now, the timeout will be hard coded'''

        state = element.is_enabled()
        timeout = 30
        current_time = 0
        while state is False and current_time < timeout:
            time.sleep(.2)
            state = element.is_enabled()
            current_time += .2

    def handle_alert(self, alert_action, child_window, alert_type=None, message_array=None,):
        ''' This function still needs some work.  auth alerts, and input text alerts still need to be handled'''
        action = None
        if alert_type is None:
            if alert_action == 'accept':
               Alert(self.driver).accept()
               action = "Click accept button on alert"
            elif alert_action == 'dismiss':
                Alert(self.driver).dismiss()
                action = "Click dismiss button on alert"
            else:
                raise Exception('Unknown alert type')
        print(action)
        return action

    def change_window_connection(self):
        self.driver.switch_to_window(self.driver.window_handles[-1])
        # title = self.driver.title
        # print('step')

    def click_object(self, param_array, child_window):

        element = self.ei.uniquely_identify_element(param_array)

        # Determine the human readable element name
        if str(self.ei.get_element_type(element)) == 'checkbox' or str(self.ei.get_element_type(element)) == 'radio':
            text_value = str(self.find_html_for(element.get_attribute('id')))
        elif str(self.ei.get_element_type(element)) == 'submit':
            text_value = element.get_attribute('value')
        elif element.tag_name == 'img':
            text_value = element.get_attribute('alt')
        else:
            text_value = element.get_attribute('innerText').strip()

        if element is not None:
            action = "Click the '" + text_value + "' " + str(self.ei.get_element_type(element))
            self.__wait_for_post_back_to_complete(element)
            self.driver.execute_script('return arguments[0].scrollIntoView();', element)
            self.driver.execute_script(' window.scrollBy(0, -150);')
            element.click()
            if child_window:
                self.change_window_connection()
            print(action)
            return action

    def enter_text(self, param_array, text_value, child_window):

        element = self.ei.uniquely_identify_element(param_array)

        if element is not None:
            # Determine if element is visible
            action = "Enter '" + str(text_value) + "' in the '" + str(self.find_html_for(element.get_attribute('id'))) + "' textbox"
            self.__wait_for_post_back_to_complete(element)
            self.driver.execute_script('return arguments[0].scrollIntoView();', element)
            self.driver.execute_script(' window.scrollBy(0, -100);')
            element.click()
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            ActionChains(self.driver).key_down(Keys.BACKSPACE).perform()
            element.send_keys(text_value)
            if child_window:
                self.change_window_connection()
            print(action)
            return action

    def select_option(self, param_array, selection_value, selection_type, child_window, multiline=None):

        action = None

        element = self.ei.uniquely_identify_element(param_array)

        if element is not None:
            self.__wait_for_post_back_to_complete(element)
            self.driver.execute_script('return arguments[0].scrollIntoView();', element)
            self.driver.execute_script(' window.scrollBy(0, -100);')
            selection = Select(element)
            options = selection.options
            acted_upon_options = self.__determine_acted_upon_option(options, selection_value, selection_type)
            if selection_type.lower() == "index":
                action = "Select '" + acted_upon_options + "' from the '" + str(self.find_html_for(element.get_attribute('id'))) + "' dropdown"
                selection.select_by_index(selection_value)
            elif selection_type.lower() == "text":
                action = "Select '" + acted_upon_options + "' from the '" + str(self.find_html_for(element.get_attribute('id'))) + "' dropdown"
                selection.select_by_visible_text(selection_value)
            elif selection_type.lower() == "value":
                action = "Select '" + acted_upon_options + "' from the '" + str(self.find_html_for(element.get_attribute('id'))) + "' dropdown"
                selection.select_by_value(selection_value)
            elif selection_type.lower() == "deindex":
                action = "Deselect '" + acted_upon_options + "' from the '" + str(self.find_html_for(element.get_attribute('id'))) + "' dropdown"
                selection.deselect_by_index(selection_value)
            elif selection_type.lower() == "detext":
                action = "Deselect '" + acted_upon_options + "' from the '" + str(self.find_html_for(element.get_attribute('id'))) + "' dropdown"
                selection.deselect_by_visible_text(selection_value)
            elif selection_type.lower() == "devalue":
                action = "Deselect '" + acted_upon_options + "' from the '" + str(self.find_html_for(element.get_attribute('id'))) + "' dropdown"
                selection.deselect_by_value(selection_value)
            elif selection_type.lower == "deall":
                action = "Deselected all values from the '" + str(self.find_html_for(element.get_attribute('id'))) + "' dropdown"
                selection.deselect_all()
            else:
                # This should really just be reported and not raise an exception
                raise Exception("Unknown selection type.")
        if child_window:
            self.change_window_connection()
        print(action)
        return action

    def __determine_acted_upon_option(self, options, selection_value, selection_type):
        acted_upon_options = None
        if selection_type == 'devalue':
            selection_type = 'value'
        elif selection_type == 'detext':
            selection_type = 'text'
        elif selection_type == 'deindex':
            selection_type = 'index'
        test = type(selection_value)
        if type(selection_value) is str:
            for option in options:
                if selection_value == option.get_attribute(selection_type):
                    if acted_upon_options is None:
                        acted_upon_options = str(option.text)
                    else:
                        acted_upon_options += ', ' + str(option.text)
        else:
            for value in selection_value:
                for option in options:
                    if value == option.get_attribute(selection_type):
                        if acted_upon_options is None:
                            acted_upon_options = str(option.text)
                        else:
                            acted_upon_options += ', ' + str(option.text)
        return acted_upon_options
