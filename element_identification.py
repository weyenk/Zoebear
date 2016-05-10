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
                if len(self.driver.find_elements_by_xpath(re.sub('\s.*', '', attach_name))) > 0:
                    element = self.driver.find_elements_by_xpath(re.sub('\s.*', '', attach_name))
            elif attach_name.startswith("#") and id_type != 'text()':
                # Contains
                if len(self.driver.find_elements_by_xpath("//*[contains(@" + id_type + ", '" + re.sub('^#', '', attach_name) + "')]")) > 0:
                    element = self.driver.find_elements_by_xpath("//*[contains(@" + id_type + ", '" + re.sub('^#', '', attach_name) + "')]")
            elif attach_name.startswith("#") and id_type == 'text()':
                # Innertext
                if len(self.driver.find_elements_by_xpath("//*[contains(text(), '" + re.sub('^#', '', attach_name) + "')]")) > 0:
                    element = self.driver.find_elements_by_xpath("//*[contains(text(), '" + re.sub('^#', '', attach_name) + "')]")
            elif id_type.lower() == 'text()':
                if len(self.driver.find_elements_by_xpath("//*[text() = '" + attach_name + "']")) > 0:
                    element = self.driver.find_elements_by_xpath("//*[text() = '" + attach_name + "']")
            else:
                # Generic Search
                if len(self.driver.find_elements_by_xpath("//*[@" + id_type + "='" + attach_name + "']")) > 0:
                    element = self.driver.find_elements_by_xpath("//*[@" + id_type + "='" + attach_name + "']")

            # print(attach_name + ': ' + str(len(element)) + ' element(s) found')
            if len(element) <= 0:
                return None
            else:
                return element

        def __remove_nonvisible_elements(self, list_of_elements):
            scrubbed_list = []
            for element in list_of_elements:
                if element.is_displayed():
                    scrubbed_list.append(element)
            return scrubbed_list

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
                if found_elements is not None:
                    found_elements = self.__remove_nonvisible_elements(found_elements)
                    if found_elements is not None:
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
            ''' This portion makes the assumption that only two lists exist which is incorrect'''
            if len(all_found_elements) == 1:
                matching_element = all_found_elements[0][0]
                return matching_element
            elif all_found_elements[0] == all_found_elements[1]:
                matching_element = all_found_elements[0][0]
                return matching_element
            else:
                matching_element = self.__complex_element_match(all_found_elements)
                return matching_element

        def __complex_element_match(self, all_found_elements):
            matches = {}
            matching_element = None
            list_total = len(all_found_elements) - 1
            i = 0
            # Loop over all lists
            while i <= list_total:
                j = 0
                # Loop over all lists again
                while j <= list_total:
                    # verify you are not comparing the list against itself
                    if i != j:
                        # compare two lists
                        for felement in all_found_elements[i]:
                            for selement in all_found_elements[j]:
                                if felement == selement:
                                    if len(matches) <= 0:  # No elements in dictionary
                                        matches[felement] = (felement, 1)
                                    else:
                                        if felement in matches.keys():  # Already in the dictionary, increase count
                                            match = matches.get(felement)
                                            new_count = match[1] + 1
                                            matches[felement] = (felement, new_count)
                                        else: # Not already in dictionary, add it
                                            matches[felement] = (felement, 1)
                    j += 1
                i += 1
            for match in matches.values():
                if matching_element is None:
                    matching_element = match
                else:
                    if matching_element[1] < match[1]:
                        matching_element = match
            if len(matching_element) > 0:
                return matching_element[0]
            else:
                print('Not enough information given to uniquely identify element')

        def find_html_for(self, for_id):
            label_list = self.driver.find_elements_by_xpath("//*[@for='" + for_id + "']")
            # This needs work.  Currently its returning the first label
            if not len(label_list) > 1 and not len(label_list) <= 0:
                return label_list[0].get_attribute('innerText')
            else:
                if label_list is not None:
                    concat_label = None
                    for label in label_list:
                        concat_label += (' ' + label)
                        return concat_label
                else:
                    print('Could not find label for ' + for_id)

        def get_element_type(self, element):
            # Find object type. Untested
            if element is not None:
                if element.tag_name == 'a':
                    element_type = 'link'
                elif element.tag_name == 'input':
                    element_type = element.get_attribute('type')
                else: # Generic items will use tagname
                    element_type = element.tag_name

                if element_type == 'None' or '':
                    print('further work needs to be done here')
                else:
                    return element_type

        def is_page_ready(self):
            print('stop')