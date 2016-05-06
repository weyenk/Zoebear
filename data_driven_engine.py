import json
import re
from element_interaction import ElementInteraction
from selenium import webdriver

class DataDrivenEngine(ElementInteraction):

    def __init__(self, name, path):
        self.script_name = name
        self.file_path = path
        file = open(self.file_path, 'r')
        raw_file_data = file.read()
        self.json_obj = json.loads(raw_file_data)


    def __parse_data(self, to_be_parsed):
        results = re.findall("'(\w+.*?)'", to_be_parsed)
        if results:
            # print(results)
            return results
        else:
            return None

    def run_script(self):

        # Instantiate webdriver
        if len(self.json_obj['browsers']) > 0:
            browser_count = len(self.json_obj['browsers']) - 1
            i = 0
            while i <= browser_count:
                browser_objects = self.__run_browsers(i)
                # Gather site information
                if len(self.json_obj['sites']) > 0:
                    site_count = len(self.json_obj['sites']) - 1
                    j = 0
                    while j <= site_count:
                        self.__run_sites(j, browser_objects['driver'])
                        # Pass data to ei
                        if len(self.json_obj['data']) > 0:
                            self.__run_data(browser_objects['ei'])
                        else:
                            raise Exception('No data too be tested')
                        j += 1
                else:
                    raise Exception('No sites too be tested')
                i += 1
        else:
            raise Exception('No browsers too be tested')


    def __run_browsers(self, counter):
        # Not all drivers are tested, specifically mobile and apple
        if str(self.json_obj['browsers'][counter]['name']).lower() == 'chrome':
            self.driver = webdriver.Chrome(self.json_obj['browsers'][counter]['location'])
        elif str(self.json_obj['browsers'][counter]['name']).lower() == 'opera':
            self.driver = webdriver.Opera(self.json_obj['browsers'][counter]['location'])
        elif str(self.json_obj['browsers'][counter]['name']).lower() == 'firefox':
            self.driver = webdriver.Firefox(self.json_obj['browsers'][counter]['location'])
        elif str(self.json_obj['browsers'][counter]['name']).lower() == 'android':
            self.driver = webdriver.Android(self.json_obj['browsers'][counter]['location'])
        elif str(self.json_obj['browsers'][counter]['name']).lower() == 'ios':
            self.driver = webdriver.Remote(self.json_obj['browsers'][counter]['location'])
        elif str(self.json_obj['browsers'][counter]['name']).lower() == 'internet explorer':
            self.driver = webdriver.Ie(self.json_obj['browsers'][counter]['location'])
        elif str(self.json_obj['browsers'][counter]['name']).lower() == 'edge':
            self.driver = webdriver.Edge(self.json_obj['browsers'][counter]['location'])
        elif str(self.json_obj['browsers'][counter]['name']).lower() == 'safari':
            self.driver = webdriver.Safari(self.json_obj['browsers'][counter]['location'])
        else:
            raise Exception(str(self.json_obj['browsers'][counter]['name']) + ' is not a supported browser')
        self.ei = ElementInteraction(self.driver)
        return {'driver': self.driver, 'ei': self.ei}


    def __run_sites(self, counter, driver):
        driver.get(self.json_obj['sites'][counter]['url'])

    def __run_data(self, ei):
        # Loop through steps
        i = 0
        while i < len(self.json_obj['data']):
            for obj in self.json_obj['data']:
                if obj['order'] == i + 1:
                    results = self.__parse_data(str(obj['identifier']))
                    if obj['action'] == "click object":
                        ei.click_object(results)
                    elif obj['action'] == "enter text":
                        ei.enter_text(results, obj['text value'])
                    elif obj['action'] == "select option":
                        ei.select_option(results, obj['selection value'], obj['selection type'])
                    else:
                        raise Exception("Step " + obj['order'] + " does not have a known action type.")
            i += 1

        print(self.json_obj)

    def quit(self):
        self.driver.quit()
