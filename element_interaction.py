from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import hashlib
import re
from element_identification import ElementIdentification


class ElementInteraction(ElementIdentification):


    def __init__(self, driver):
        self.driver = driver
        self.ei = ElementIdentification(self.driver)

    def click_object(self, attach_name, second_attach_name=None):
        element = None

        if second_attach_name is not None:
            element = self.ei.uniquely_identify_element(attach_name, second_attach_name)
        else:
            element = self.ei.uniquely_identify_element(attach_name)

        if element is None:
            print("Could not find an object with '" + attach_name + "' as an identifying marker.")
        else:
            # print("Click the '" + element.text + "' " + element_type)
            element.click()

    def enter_text(self, attach_name, text, second_attach_name=None):
        element = None

        if second_attach_name is not None:
            element = self.ei.uniquely_identify_element(attach_name, second_attach_name)
        else:
            element = self.ei.uniquely_identify_element(attach_name)

        if element is None:
            print("Could not find a textbox with '" + attach_name + "' as an identifying marker.")
        else:
            print("Enter '" + text + "' in the '" + self.find_html_for(element.get_attribute('id')) + "' textbox")
            element.send_keys(text)

    def select_option(self, attach_name, value, selection_type, second_attach_name=None, multiline=None):
        element = None

        if second_attach_name is not None:
            element = self.ei.uniquely_identify_element(attach_name, second_attach_name)
        else:
            element = self.ei.uniquely_identify_element(attach_name)

        if element is None:
            print("Could not find a dropdown with '" + attach_name + "' as an identifying marker.")
        else:
            selection = Select(element)
            if selection_type.lower() == "index":
                selection.select_by_index(value)
                # print("Select '" + + "' from the '" + + "' dropdown")
            elif selection_type.lower() == "text":
                selection.select_by_visible_text(value)
                # print("Select '" + + "' from the '" + + "' dropdown")
            elif selection_type.lower() == "value":
                selection.select_by_value(value)
                # print("Select '" + + "' from the '" + + "' dropdown")
            elif selection_type.lower() == "deindex":
                selection.deselect_by_index(value)
                # print("Select '" + + "' from the '" + + "' dropdown")
            elif selection_type.lower() == "detext":
                selection.deselect_by_visible_text(value)
                # print("Select '" + + "' from the '" + + "' dropdown")
            elif selection_type.lower() == "devalue":
                selection.deselect_by_value(value)
                # print("Select '" + + "' from the '" + + "' dropdown")
            elif selection_type.lower == "deall":
                selection.deselect_all()
                # print("Deselected all values from the '" + + "' dropdown")
            else:
                raise Exception("Unknown selection type.  Attach name:" + attach_name)


    def compare_hash(self, preclick, postclick):
        first = hashlib.md5  # (preclick).hexdigest()
        first.update(preclick)
        first.digest()
        second = hashlib.md5(postclick).hexdigest()
        timeout = 0
        if preclick.id != postclick.id:  # & timeout != True:
            hashlib.md5(self.driver.find_element_by_tagname('html')).hexdigist()
            return True
        else:
            return False
            timeout += 1
            if timeout > 100:
                timeout = False
