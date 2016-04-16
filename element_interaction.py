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
            print(u"Could not find an object with '{0:s}' as an identifying marker.".format(attach_name))
        else:
            print(u"Click the '{0:s}' object".format(element.text))
            element.click()

    def enter_text(self, attach_name, text, second_attach_name=None):
        element = None

        if second_attach_name is not None:
            element = self.ei.uniquely_identify_element(attach_name, second_attach_name)
        else:
            element = self.ei.uniquely_identify_element(attach_name)

        if element is None:
            print("Could not find a textbox with '%s' as an identifying marker.".format(attach_name))
        else:
            #print(u"Enter '{0:s}' in the '{1:s}' textbox".format(text, self.find_html_for(element.id)))
            element.send_keys(text)

    def select_option(self, attach_name, value, selection_type, second_attach_name=None, multiline=None):
        element = None

        if second_attach_name is not None:
            element = self.ei.uniquely_identify_element(attach_name, second_attach_name)
        else:
            element = self.ei.uniquely_identify_element(attach_name)

        if element is None:
            print(u"Could not find a dropdown with '{0:s}' as an identifying marker.".format(attach_name))
        else:
            selection = Select(element)
            if selection_type.lower() == "index":
                selection.select_by_index(value)
                #print(u"Select '{0:s}' from the '{1:s} dropdown'".format())
            elif selection_type.lower() == "text":
                selection.select_by_visible_text(value)
            elif selection_type.lower() == "value":
                selection.select_by_value(value)
            elif selection_type.lower() == "deindex":
                selection.deselect_by_index(value)
            elif selection_type.lower() == "detext":
                selection.deselect_by_visible_text(value)
            elif selection_type.lower() == "devalue":
                selection.deselect_by_value(value)
            elif selection_type.lower == "deall":
                selection.deselect_all()
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
            print("Could not find a link with '%s' as an identifying marker.", attach_name)