from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import re
from element_identification import ElementIdentification
import pickle


class ElementInteraction(ElementIdentification):

    def __init__(self, driver):
        self.driver = driver
        self.ei = ElementIdentification(self.driver)

    def click_object(self, param_array):
        element = None

        element = self.ei.uniquely_identify_element(param_array)

        if element is not None:
            if element.is_displayed():
                print("Click the '" + element.text + "' " + self.ei.get_element_type(element))
                element.click()
            else:
                raise Exception('Element is present but not visible. ID: ' + element.get_attribute('id'))

    def enter_text(self, param_array, text_value):

        element = self.ei.uniquely_identify_element(param_array)

        if element is not None:
            # Determine if element is visible
            if element.is_displayed():
                print("Enter '" + str(text_value) + "' in the '" + str(self.find_html_for(element.get_attribute('id'))) + "' textbox")
                element.send_keys(text_value)
            else:
                # This should really check if the element has an ID before assuming.  Perhaps make a method to check
                raise Exception('Element is present but not visible. ID: ' + element.get_attribute('id'))

    def select_option(self, param_array, selection_value, selection_type, multiline=None):

        element = self.ei.uniquely_identify_element(param_array)

        if element is not None:
            selection = Select(element)
            if selection_type.lower() == "index":
                if element.is_displayed():
                    selection.select_by_index(selection_value)
                    print("Select '" + selection.all_selected_options + "' from the '" + self.find_html_for(element.get_attribute('id')) + "' dropdown")
                else:
                    raise Exception('Element is present but not visible. ID: ' + element.get_attribute('id'))
            elif selection_type.lower() == "text":
                if element.is_displayed():
                    selection.select_by_visible_text(selection_value)
                    print("Select '" + selection_value + "' from the '" + self.find_html_for(element.get_attribute('id')) + "' dropdown")
                else:
                    raise Exception('Element is present but not visible. ID: ' + element.get_attribute('id'))
            elif selection_type.lower() == "value":
                if element.is_displayed():
                    selection.select_by_value(selection_value)
                    print("Select '" + selection.all_selected_options + "' from the '" + self.find_html_for(element.get_attribute('id')) + "' dropdown")
                else:
                    raise Exception('Element is present but not visible. ID: ' + element.get_attribute('id'))
            elif selection_type.lower() == "deindex":
                if element.is_displayed():
                    print("Deselect '" + selection.all_selected_options + "' from the '" + self.find_html_for(element.get_attribute('id')) + "' dropdown")
                    selection.deselect_by_index(selection_value)
                else:
                    raise Exception('Element is present but not visible. ID: ' + element.get_attribute('id'))
            elif selection_type.lower() == "detext":
                if element.is_displayed():
                    print("Deselect '" + selection_value + "' from the '" + self.find_html_for(element.get_attribute('id')) + "' dropdown")
                    selection.deselect_by_visible_text(selection_value)
                else:
                    raise Exception('Element is present but not visible. ID: ' + element.get_attribute('id'))
            elif selection_type.lower() == "devalue":
                if element.is_displayed():
                    print("Deselect '" + selection.all_selected_options + "' from the '" + self.find_html_for(element.get_attribute('id')) + "' dropdown")
                    selection.deselect_by_value(selection_value)
                else:
                    raise Exception('Element is present but not visible. ID: ' + element.get_attribute('id'))
            elif selection_type.lower == "deall":
                if element.is_displayed():
                    selection.deselect_all()
                    print("Deselected all values from the '" + self.find_html_for(element.get_attribute('id')) + "' dropdown")
                else:
                    raise Exception('Element is present but not visible. ID: ' + element.get_attribute('id'))
            else:
                # This should really just be reported and not raise an exception
                raise Exception("Unknown selection type.")

    def assert_page_changed(self, preclick, postclick):
        pickled_preclick = pickle.dumps(preclick)
        pickled_postclick = pickle.dumps(postclick)
        if pickled_preclick == pickled_postclick:
            return True
        else:
            return False
