from element_identification import ElementIdentification
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
import pickle
import time
import re

class ElementInteraction(ElementIdentification):

    def __init__(self, driver):
        self.driver = driver
        self.ei = ElementIdentification(self.driver)

    '''def __soft_assert_page_changed(self, preclick, postclick):
        pickled_preclick = pickle.dumps(preclick)
        pickled_postclick = pickle.dumps(postclick)
        if pickled_preclick == pickled_postclick:
            return True
        else:
            return False'''

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

    def __wait_for_post_back_to_complete(self, element, timeout=None):
        # Init state
        state = element.is_enabled()
        if timeout is None:
            timeout = 30
        current_time = 0

        # Continuously check state until timeout or ready
        while state is False and current_time < timeout:
            time.sleep(.2)
            state = element.is_enabled()
            current_time += .2

    def change_window_connection(self):

        # Select the last active window
        self.driver.switch_to_window(self.driver.window_handles[-1])

    def handle_alert(self, obj):
        # Set parameters
        step = obj.get('order')
        alert_action = obj.get('alert_action')
        if alert_action is None:
            raise Exception('No child_window for step number' + str(step))
        child_window = obj.get('child_window')
        if child_window is None:
            raise Exception('No child_window for step number' + str(step))
        alert_type = obj.get('alert_type')
        message_array = obj.get('message_array')

        action = None
        if alert_type is None:

            # Standard 'Ok', 'Cancel' alert
            if alert_action == 'accept':
                Alert(self.driver).accept()
                action = "Click accept button on alert"
            elif alert_action == 'dismiss':
                Alert(self.driver).dismiss()
                action = "Click dismiss button on alert"
            else:
                raise Exception('Unknown generic alert type')
        elif alert_type == 'auth':

            # Authentication alert
            if type(message_array) is 'list':
                Alert(self.driver).authenticate(message_array[0], message_array[1])
            elif type(message_array) is 'dict':
                Alert(self.driver).authenticate(message_array.get('username', 'Username not found'), message_array.get('password', 'Password not found'))
            action = 'Entered username and password into the alert.'
        elif alert_type == 'custom':

            # Future home of customer alerts when they are needed.
            print('No custom alerts exist at this time')
            action = 'No custom alerts exist at this time'

        # Determine if action changes browser count
        if child_window:
            self.change_window_connection()

        print(action)
        return action

    def click_object(self, obj):
        # Set local parameters
        step = obj.get('order')
        identifier_dict = obj.get('identifier')
        if identifier_dict is None:
            raise Exception('No identifier for step number ' + str(step))
        child_window = obj.get('child_window')
        if child_window is None:
            raise Exception('No child_window for step number' + str(step))

        element = self.ei.uniquely_identify_element(identifier_dict)

        # Report no element found
        if element is None:
            action = 'No element found for step ' + str(step)
            return action

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

            # Prepare element for action
            self.__wait_for_post_back_to_complete(element, obj.get('timeout'))
            self.driver.execute_script('return arguments[0].scrollIntoView();', element)
            self.driver.execute_script('window.scrollBy(0, -150);')

            element.click()

            # Determine if action changes browser count
            if child_window:
                self.change_window_connection()

            print(action)
            return action

    def enter_text(self, obj):
        # Set local parameters
        step = obj.get('order')
        identifier_dict = obj.get('identifier')
        if identifier_dict is None:
            raise Exception('No identifier for step number ' + str(step))
        child_window = obj.get('child_window')
        if child_window is None:
            raise Exception('No child_window for step number' + str(step))
        text_value = obj.get('text_value')

        element = self.ei.uniquely_identify_element(identifier_dict)

        # Report no element found
        if element is None:
            action = 'No element found for step ' + str(step)
            return action

        if element is not None:
            # Determine if element is visible
            action = "Enter '" + str(text_value) + "' in the '" + str(self.find_html_for(element.get_attribute('id'))) + "' textbox"

            # Prepare element for action
            self.__wait_for_post_back_to_complete(element, obj.get('timeout'))
            self.driver.execute_script('return arguments[0].scrollIntoView();', element)
            self.driver.execute_script('window.scrollBy(0, -100);')

            # Clear existing text and send new text
            element.clear()
            element.send_keys(text_value)

            # Determine if action changes browser count
            if child_window:
                self.change_window_connection()

            print(action)
            return action

    def select_option(self, obj):
        # Set local parameters
        step = obj.get('order')
        identifier_dict = obj.get('identifier')
        if identifier_dict is None:
            raise Exception('No identifier for step number ' + str(step))
        child_window = obj.get('child_window')
        if child_window is None:
            raise Exception('No child_window for step number' + str(step))
        selection_value = obj.get('selection_value')
        if selection_value is None:
            raise Exception('No selection_value for step number' + str(step))
        selection_type = obj.get('selection_type')
        if selection_type is None:
            raise Exception('No selection_type for step number' + str(step))
        multiline = obj.get('multiline')
        action = None

        element = self.ei.uniquely_identify_element(identifier_dict)

        # Report no element found
        if element is None:
            action = 'No element found for step ' + str(step)
            return action

        if element is not None:

            # Prepare element for action
            self.__wait_for_post_back_to_complete(element, obj.get('timeout'))
            self.driver.execute_script('return arguments[0].scrollIntoView();', element)
            self.driver.execute_script(' window.scrollBy(0, -100);')
            selection = Select(element)
            options = selection.options
            acted_upon_options = self.__determine_acted_upon_option(options, selection_value, selection_type)

            # Determine how we are interacting with the select
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

        # Determine if action changes browser count
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
