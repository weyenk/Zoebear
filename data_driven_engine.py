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
        # self.driver = webdriver.Chrome("/usr/bin/chromedriver")
        # self.ei = ElementInteraction(self.driver)

    def __parse_data(self, to_be_parsed):
        results = re.findall("'(\w+.*?)'", to_be_parsed)
        if results:
            # print(results)
            return results
        else:
            return None

    def run_script(self):

        # Instantiate webdriver
        if len(self.json_obj['browser']) > 0:
            self.__run_browsers()
        else:
            raise Exception('No browsers being tested')
        # Gather site information
        self.__run_sites()
        # Determine if user information is required and obtain any required files
        self.__run_users()
        # Pass data to ei
        self.__run_data()

    def __run_browsers(self):
        pass

    def __run_sites(self):
        pass

    def __run_users(self):
        pass

    def __run_data(self, ei):
        # Loop through steps
        i = 0
        while i < len(self.json_obj['data']):
            for obj in self.json_obj['data']:
                if obj['order'] == i + 1:
                    results = self.__parse_data(str(obj['identifier']))
                    if obj['action'] == "click object":
                        pass
                        ei.click_object(results)
                    elif obj['action'] == "enter text":
                        pass
                        ei.enter_text(results, obj['text value'])
                    elif obj['action'] == "select option":
                        pass
                        ei.select_option(results, obj['selection value'], obj['selection type'])
                    else:
                        raise Exception("Step " + obj['order'] + " does not have a known action type.")
            i += 1

        print(self.json_obj)
