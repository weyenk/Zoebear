import re
from multiprocessing import Pipe
from element_map import ElementMap

class ElementIdentification:

        def __init__(self, driver):
            self.driver = driver

        def __dynamic_wait(self):
            pass

        def __wait_for_page_load(self):
            old_page = self.driver.find_elements_by_tagname('html')
            new_page = self.driver.find_elements_by_tagname('html')
            while old_page.id == new_page.id:
                new_page = self.driver.find_elements_by_tagname('html')

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

        def uniquely_identify_element(self, identifier_dict):

            # Establish variables
            matching_element = None
            all_found_elements = []
            complex_match = False

            # Convert dict of any size into a list of tuples
            ident_items = identifier_dict.items()
            for ident_item in ident_items:
                found_elements = self.find_element(ident_item[0], ident_item[1])
                if found_elements is not None:
                    found_elements = self.__remove_nonvisible_elements(found_elements)
                    if found_elements is not None:
                        all_found_elements.append(found_elements)

            # Determine element counts in each.  If either list is greater than one that mark complex match
            i = 0
            j = len(all_found_elements) - 1
            while i <= j and complex_match is False:
                if len(all_found_elements[i]) > 1:
                    complex_match = True
                else:
                    i += 1

            # Determine is only one element is found, or if additional matching is needed
            if len(all_found_elements) == 1:
                matching_element = all_found_elements[0][0]
                return matching_element
            else:
                matching_element = self.__complex_element_match(all_found_elements)
                if matching_element == "no match":
                    print(identifier_dict)
                else:
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
            if matching_element is not None:
                return matching_element[0]
            else:
                return "no match"

        def find_html_for(self, for_id):
            label_list = self.driver.find_elements_by_xpath("//*[@for='" + for_id + "']")

            # If only a single list return it, else concat all labels found
            if not len(label_list) > 1 and not len(label_list) <= 0:
                return label_list[0].get_attribute('innerText')
            else:
                if label_list is not None:
                    concat_label = None
                    for label in label_list:
                        if concat_label is None:
                            concat_label = str(label.get_attribute('innerText')).strip()
                        else:
                            concat_label += ' ' + str(label.get_attribute('innerText')).strip()
                    return concat_label
                else:
                    print('Could not find label for ' + for_id)

        def get_element_type(self, element):
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

        @staticmethod
        def create_id_dict(tags: list, pipe=None):
            id_dict = {}
            i = 0
            for tag in tags:
                if not tag.get_attribute('type') == 'hidden':
                    id_dict[tag.get_attribute('id')] = i
                    i += 1
            if pipe is None:
                return id_dict
            else:
                pipe.send(id_dict)
                pipe.close()

        @staticmethod
        def create_href_dict(tags: list, pipe=None):
            href_dict = {}
            i = 0
            for tag in tags:
                if not tag.get_attribute('type') == 'hidden':
                    href_dict[tag.get_attribute('herf')] = i
                    i += 1
            if pipe is None:
                return href_dict
            else:
                pipe.send(href_dict)
                pipe.close()

        @staticmethod
        def create_name_dict(tags: list, pipe=None):
            name_dict = {}
            i = 0
            for tag in tags:
                if not tag.get_attribute('type') == 'hidden':
                    name_dict[tag.get_attribute('name')] = i
                    i += 1
            if pipe is None:
                return name_dict
            else:
                pipe.send(name_dict)
                pipe.close()

        @staticmethod
        def create_src_dict(tags: list, pipe=None):
            src_dict = {}
            i = 0
            for tag in tags:
                if not tag.get_attribute('type') == 'hidden':
                    src_dict[tag.get_attribute('src')] = i
                    i += 1
            if pipe is None:
                return src_dict
            else:
                pipe.send(src_dict)
                pipe.close()

        @staticmethod
        def create_alt_dict(tags: list, pipe=None):
            alt_dict = {}
            i = 0
            for tag in tags:
                if not tag.get_attribute('type') == 'hidden':
                    alt_dict[tag.get_attribute('alt')] = i
                    i += 1
            if pipe is None:
                return alt_dict
            else:
                pipe.send(alt_dict)
                pipe.close()

        @staticmethod
        def create_title_dict(tags: list, pipe=None):
            title_dict = {}
            i = 0
            for tag in tags:
                if not tag.get_attribute('type') == 'hidden':
                    title_dict[tag.get_attribute('title')] = i
                    i += 1
            if pipe is None:
                return title_dict
            else:
                pipe.send(title_dict)
                pipe.close()

        @staticmethod
        def create_text_dict(tags: list, pipe=None):
            text_dict = {}
            i = 0
            for tag in tags:
                if not tag.get_attribute('type') == 'hidden':
                    text_dict[tag.get_attribute('innerText')] = i
                    i += 1
            if pipe is None:
                return text_dict
            else:
                pipe.send(text_dict)
                pipe.close()

        @staticmethod
        def create_value_dict(tags: list, pipe=None):
            value_dict = {}
            i = 0
            for tag in tags:
                if not tag.get_attribute('type') == 'hidden':
                    value_dict[tag.get_attribute('value')] = i
                    i += 1
            if pipe is None:
                return value_dict
            else:
                pipe.send(value_dict)
                pipe.close()

        @staticmethod
        def create_class_dict(tags: list, pipe=None):
            class_dict = {}
            i = 0
            for tag in tags:
                if not tag.get_attribute('type') == 'hidden':
                    class_dict[tag.get_attribute('class')] = i
                    i += 1
            if pipe is None:
                return class_dict
            else:
                pipe.send(class_dict)
                pipe.close()