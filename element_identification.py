import re
from selenium.selenium import selenium
import pickle

class ElementIdentification:

        def __init__(self, driver):
            self.driver = driver

        def is_element_present(self, attach_name):
            # CSS selector
            if len(self.driver.find_elements_by_css_selector(attach_name)) > 0:
                return True
            # ID
            elif len(self.driver.find_elements_by_id(attach_name)) > 0:
                return True
            # Link text
            elif len(self.driver.find_elements_by_link_text(attach_name)) > 0:
                return True
            # Partial link text
            elif len(self.driver.find_elements_by_partial_link_text(attach_name)) > 0:
                return True
            # Class name
            elif len(self.driver.find_elements_by_class_name(re.sub("\s.*", "", attach_name))) > 0:
                return True
            # XPATH
            elif len(self.driver.find_elements_by_xpath(re.sub("\s.*", "", attach_name))) > 0:
                return True
            else:
                print("Could not find a link with '" + attach_name + "' as an identifying marker.")

        def find_element(self, attach_name):
            element = []

            # ID
            if len(self.driver.find_elements_by_id(attach_name)) > 0:
                element = self.driver.find_elements_by_id(attach_name)
            # CSS selector
            elif len(self.driver.find_elements_by_css_selector(attach_name)) > 0:
                element = self.driver.find_elements_by_css_selector(attach_name)
            # Link text
            elif len(self.driver.find_elements_by_link_text(attach_name)) > 0:
                element = self.driver.find_elements_by_link_text(attach_name)
            # Partial link text
            elif len(self.driver.find_elements_by_partial_link_text(attach_name)) > 0:
                element = self.driver.find_elements_by_partial_link_text(attach_name)
            # Class name
            elif len(self.driver.find_elements_by_class_name(re.sub("\s.*", "", attach_name))) > 0:
                element = self.driver.find_elements_by_class_name(re.sub("\s.*", "", attach_name))
            # XPATH
            elif len(self.driver.find_elements_by_xpath(re.sub("\s.*", "", attach_name))) > 0:
                element = self.driver.find_elements_by_xpath(re.sub("\s.*", "", attach_name))
            # Value
            elif len(self.driver.find_elements_by_xpath("//*[@value='" + attach_name + "']")) > 0:
                element = self.driver.find_elements_by_xpath("//*[@value='" + attach_name + "']")
            # Text
            elif len(self.driver.find_elements_by_xpath("//*[@text='" + attach_name + "']")) > 0:
                element = self.driver.find_elements_by_xpath("//*[@text='" + attach_name + "']")
            # Name
            elif len(self.driver.find_elements_by_xpath("//*[@name='" + attach_name + "']")) > 0:
                element = self.driver.find_elements_by_xpath("//*[@name='" + attach_name + "']")
            # Text content. Untested
            elif len(self.driver.find_elements_by_xpath("//*[contains(text(), '" + attach_name + "')]")) > 0:
                element = self.driver.find_elements_by_xpath("//*[contains(text(), '" + attach_name + "')]")
            # Href
            elif len(self.driver.find_elements_by_xpath("//*[@href='" + attach_name + "']")) > 0:
                element = self.driver.find_elements_by_xpath("//*[@href='" + attach_name + "']")
            # Src
            elif len(self.driver.find_elements_by_xpath("//*[@src='" + attach_name + "']")) > 0:
                element = self.driver.find_elements_by_xpath("//*[@src='" + attach_name + "']")
            # Alt
            elif len(self.driver.find_elements_by_xpath("//*[@alt='" + attach_name + "']")) > 0:
                element = self.driver.find_elements_by_xpath("//*[@alt='" + attach_name + "']")
            # Title
            elif len(self.driver.find_elements_by_xpath("//*[@title='" + attach_name + "']")) > 0:
                element = self.driver.find_elements_by_xpath("//*[@title='" + attach_name + "']")
            print(attach_name + ": " + str(len(element)) + " element(s) found")
            if len(element) <= 0:
                return None
            else:
                return element

        def uniquely_identify_element(self, attach_name, second_attach_name=None):
            # Establish variables
            matching_element = None
            first_element = []
            second_element = []
            complex_match = False

            # Find all elements that match
            first_element = self.find_element(attach_name)
            if second_attach_name is not None:
                second_element = self.find_element(second_attach_name)

            # Determine element counts in each.  If either list is greater than one that mark complex match
            if len(first_element) > 1:
                complex_match = True
            if len(second_element) > 1:
                complex_match = True
            if len(first_element) <= 0 and len(second_element) <= 0:
                print("Could not find an object with '" + attach_name + "' or '" +
                      second_attach_name + "' as an identifying markers.")

            # If neither element requires complex matching, then run basic match here
            if not complex_match:
                if len(second_element) == 0:
                    matching_element = first_element[0]
                    return matching_element
                elif first_element == second_element:
                    matching_element = first_element[0]
                    return matching_element
                elif first_element != second_element:
                    print("Could not uniquely identify an singular element with '" + attach_name +
                          "' or '" + second_attach_name + "' as an identifying markers.")
            else:
                matching_element = self.complex_element_match(first_element, second_element)
                return matching_element

        def complex_element_match(self, first_elements, second_elements):
            # Determine if either list is empty
            if len(first_elements) <= 0 or len(second_elements) <= 0:
                print("Identifying markers are not unique enough to find object")
                return None

            # Loop over the first element in the first list
            for f_element in first_elements:
                for s_element in second_elements:
                    if f_element.get_attribute('outerHTML') == s_element.get_attribute('outerHTML'):
                        return f_element
                    else:
                        continue

        def find_html_for(self, for_id):
            label_list = self.driver.find_elements_by_xpath("//*[@for='" + for_id + "']")
            for label in label_list:
                return label.text

        def derive_element_type(self, element):
            # Find object type. Untested
            if element is not None:
                element_type = element.get_attribute("type")
                if element_type is None:
                    print("further work needs to be done here")

        def is_page_ready(self):
            print("stop")