import json


class ElementMap:

    def __init__(self, driver):
        self.driver = driver

    def map_page(self):
        elements = self.driver.find_elements_by_tag_name("*")
        current_page = {}
        page_objects = []
        i = 0
        while i < len(elements):
            if elements[i].tag_name == 'a' or elements[i].tag_name == 'input' or elements[i].tag_name == 'textarea' or elements[i].tag_name == 'img' or elements[i].tag_name == 'select':
                if elements[i].get_attribute('type') != 'hidden':
                    currentObj = {}
                    currentObj['element name'] = ('element' + str(i))
                    currentObj['tagname'] = elements[i].tag_name
                    currentObj['type'] = elements[i].get_attribute('type')
                    currentObj['id'] = elements[i].get_attribute('id')
                    currentObj['src'] = elements[i].get_attribute('src')
                    currentObj['href'] = elements[i].get_attribute('href')
                    currentObj['name'] = elements[i].get_attribute('name')
                    currentObj['alt'] = elements[i].get_attribute('alt')
                    currentObj['title'] = elements[i].get_attribute('title')
                    currentObj['text content'] = elements[i].text
                    currentObj['checked'] = elements[i].get_attribute('checked')
                    currentObj['selected index'] = elements[i].get_attribute('')
                    currentObj['selected text'] = elements[i].get_attribute('')
                    currentObj['class'] = elements[i].get_attribute('class')
                    currentObj['value'] = elements[i].get_attribute('value')
                    currentObj['onclick'] = elements[i].get_attribute('onclick')
                    currentObj['onblur'] = elements[i].get_attribute('onblur')
                    currentObj['onchange'] = elements[i].get_attribute('onchange')
                    currentObj['onkeypress'] = elements[i].get_attribute('onkeypress')
                    currentObj['child window'] = elements[i].get_attribute('')
                    currentObj['html'] = elements[i].get_attribute('outerHTML')
                    page_objects.append(currentObj)
            i += 1

        current_page[self.driver.title] = page_objects

        return current_page

    def send_to_mongodb(self):
        pass

    def retrieve_from_mongodb(self):
        pass

