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
            print("Click the '" + element.text + "' " + self.ei.get_element_type(element))
            element.click()

    def enter_text(self, param_array, text_value):

        element = self.ei.uniquely_identify_element(param_array)

        if element is not None:
            print("Enter '" + text_value + "' in the '" + self.find_html_for(element.get_attribute('id')) + "' textbox")
            element.send_keys(text_value)

    def select_option(self, param_array, selection_value, selection_type, multiline=None):

        element = self.ei.uniquely_identify_element(param_array)

        if element is not None:
            selection = Select(element)
            if selection_type.lower() == "index":
                selection.select_by_index(selection_value)
                print("Select '" + selection.all_selected_options + "' from the '" + self.find_html_for(
                    element.get_attribute('id')) + "' dropdown")
            elif selection_type.lower() == "text":
                selection.select_by_visible_text(selection_value)
                print("Select '" + selection_value + "' from the '" + self.find_html_for(
                    element.get_attribute('id')) + "' dropdown")
            elif selection_type.lower() == "value":
                selection.select_by_value(selection_value)
                print("Select '" + selection.all_selected_options + "' from the '" + self.find_html_for(
                    element.get_attribute('id')) + "' dropdown")
            elif selection_type.lower() == "deindex":
                print("Deselect '" + selection.all_selected_options + "' from the '" + self.find_html_for(
                    element.get_attribute('id')) + "' dropdown")
                selection.deselect_by_index(selection_value)
            elif selection_type.lower() == "detext":
                print("Deselect '" + selection_value + "' from the '" + self.find_html_for(
                    element.get_attribute('id')) + "' dropdown")
                selection.deselect_by_visible_text(selection_value)
            elif selection_type.lower() == "devalue":
                print("Deselect '" + selection.all_selected_options + "' from the '" + self.find_html_for(
                    element.get_attribute('id')) + "' dropdown")
                selection.deselect_by_value(selection_value)
            elif selection_type.lower == "deall":
                selection.deselect_all()
                print("Deselected all values from the '" + self.find_html_for(
                    element.get_attribute('id')) + "' dropdown")
            else:
                raise Exception("Unknown selection type.  Attach name:" + attach_name)

    def assert_page_changed(self, preclick, postclick):
        pickled_preclick = pickle.dumps(preclick)
        pickled_postclick = pickle.dumps(postclick)
        if pickled_preclick == pickled_postclick:
            return True
        else:
            return False
