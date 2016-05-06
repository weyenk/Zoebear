import re
from selenium.selenium import selenium
import pickle

class ElementIdentification:

        def __init__(self, driver):
            self.driver = driver

        def find_element(self, id_type, attach_name):
            element = []

            if id_type.lower() == 'xpath':
                # XPATH
                if len(self.driver.find_elements_by_xpath(re.sub("\s.*", "", attach_name))) > 0:
                    element = self.driver.find_elements_by_xpath(re.sub("\s.*", "", attach_name))
            elif attach_name.startswith("#") and id_type != 'text()':
                # Contains
                if len(self.driver.find_elements_by_xpath("//*[contains(@" + id_type + ", '" +
                                                                  re.sub("^#", "", attach_name) + "')]")) > 0:
                    element = self.driver.find_elements_by_xpath("//*[contains(@" + id_type + ", '" +
                                                                 re.sub("^#", "", attach_name) + "')]")
            elif attach_name.startswith("#") and id_type == 'text()':
                # Innertext
                if len(self.driver.find_elements_by_xpath("//*[contains(text(), '" +
                                                                  re.sub("^#", "", attach_name) + "')]")) > 0:
                    element = self.driver.find_elements_by_xpath("//*[contains(text(), '" +
                                                         re.sub("^#", "", attach_name) + "')]")
            else:
                # Generic Search
                if len(self.driver.find_elements_by_xpath("//*[@" + id_type + "='" + attach_name + "']")) > 0:
                    element = self.driver.find_elements_by_xpath("//*[@" + id_type + "='" + attach_name + "']")

            print(attach_name + ": " + str(len(element)) + " element(s) found")
            if len(element) <= 0:
                return None
            else:
                return element

        def uniquely_identify_element(self, param_array):
            # Establish variables
            matching_element = None
            all_found_elements = []
            found_elements = []
            complex_match = False

            # Build lists of elements
            i = 0
            j = 0
            while i < len(param_array):
                found_elements = self.find_element(param_array[i], param_array[i + 1])
                all_found_elements.append(found_elements)
                j += 1
                i += 2

            # Determine element counts in each.  If either list is greater than one that mark complex match
            i = 0
            j = len(all_found_elements) - 1
            while i <= j and complex_match is False:
                if len(all_found_elements[i]) > 1:
                    complex_match = True
                else:
                    i += 1

            # If neither element requires complex matching, then run basic match here
            if not complex_match:
                if len(all_found_elements) == 1:
                    matching_element = all_found_elements[0][0]
                    return matching_element
                elif all_found_elements[0] == all_found_elements[1]:
                    matching_element = all_found_elements[0][0]
                    return matching_element

                # if first_element == second_element:
                #    matching_element = first_element[0]
                #    return matching_element
                # elif first_element != second_element:
                #    print("Could not uniquely identify an singular element with '" + attach_name +
                #          "' or '" + second_attach_name + "' as an identifying markers.")
            else:
                matching_element = self.__complex_element_match(all_found_elements)
                return matching_element

        def __complex_element_match(self, first_elements, second_elements):
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

        def get_element_type(self, element):
            # Find object type. Untested
            if element is not None:
                element_type = element.get_attribute("type")
                if element_type is None:
                    print("further work needs to be done here")
                else:
                    return element_type

        def is_page_ready(self):
            print("stop")