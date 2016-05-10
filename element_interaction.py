from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.selenium import selenium
import re
from element_identification import ElementIdentification
import pickle


class ElementInteraction(ElementIdentification):

    def __init__(self, driver):
        self.driver = driver
        self.ei = ElementIdentification(self.driver)

    def __assert_page_changed(self, preclick, postclick):
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

    def __dynamic_wait(self):
        # Wait for page to reach ready state and wait for all rendering to complete
        pass

    def __check_network_activity(self):
        # Determine if browser is still receiving informaiton
        pass

    def handle_dialog(self, param_array):
        # Determine
        #if
        pass

    def click_object(self, param_array):

        element = self.ei.uniquely_identify_element(param_array)

        # Determine the human readable element name
        if str(self.ei.get_element_type(element)) == 'checkbox' or str(self.ei.get_element_type(element)) == 'radio':
            text_value = str(self.find_html_for(element.get_attribute('id')))
        elif str(self.ei.get_element_type(element)) == 'submit':
            text_value = element.get_attribute('value')
        else:
            text_value = element.get_attribute('innerText').strip()

        if element is not None:
            print("Click the '" + text_value + "' " + str(self.ei.get_element_type(element)))
            element.click()

    def enter_text(self, param_array, text_value):

        element = self.ei.uniquely_identify_element(param_array)

        if element is not None:
            # Determine if element is visible
            print("Enter '" + str(text_value) + "' in the '" + str(self.find_html_for(element.get_attribute('id'))) + "' textbox")
            element.send_keys(text_value)

    def select_option(self, param_array, selection_value, selection_type, multiline=None):

        element = self.ei.uniquely_identify_element(param_array)

        if element is not None:
            selection = Select(element)
            if selection_type.lower() == "index":
                selection.select_by_index(selection_value)
                print("Select '" + selection.all_selected_options + "' from the '" + str(self.find_html_for(element.get_attribute('id'))) + "' dropdown")
            elif selection_type.lower() == "text":
                selection.select_by_visible_text(selection_value)
                print("Select '" + selection_value + "' from the '" + str(self.find_html_for(element.get_attribute('id'))) + "' dropdown")
            elif selection_type.lower() == "value":
                selection.select_by_value(selection_value)
                print("Select '" + selection.all_selected_options + "' from the '" + str(self.find_html_for(element.get_attribute('id'))) + "' dropdown")
            elif selection_type.lower() == "deindex":
                # This doesnt make sense.  A function needs to be written to check all the options against the user supplied indexes
                print("Deselect '" + selection.all_selected_options + "' from the '" + str(self.find_html_for(element.get_attribute('id'))) + "' dropdown")
                selection.deselect_by_index(selection_value)
            elif selection_type.lower() == "detext":
                print("Deselect '" + selection_value + "' from the '" + str(self.find_html_for(element.get_attribute('id'))) + "' dropdown")
                selection.deselect_by_visible_text(selection_value)
            elif selection_type.lower() == "devalue":
                # This doesnt make sense.  A function needs to be written to check all the options against the user supplied values
                print("Deselect '" + selection.all_selected_options + "' from the '" + str(self.find_html_for(element.get_attribute('id'))) + "' dropdown")
                selection.deselect_by_value(selection_value)
            elif selection_type.lower == "deall":
                selection.deselect_all()
                print("Deselected all values from the '" + str(self.find_html_for(element.get_attribute('id'))) + "' dropdown")
            else:
                # This should really just be reported and not raise an exception
                raise Exception("Unknown selection type.")
