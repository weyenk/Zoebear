import json
import re
from element_interaction import ElementInteraction
from selenium import webdriver
import os
import time
import datetime

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
        browser_objects = []
        start_time = time.time()
        # create output file
        output = self.__create_output_file()
        # Instantiate webdriver
        if len(self.json_obj['browsers']) > 0:
            browser_count = len(self.json_obj['browsers']) - 1
            i = 0
            # Launch i(th) browser
            while i <= browser_count:
                browser_objects = self.__run_browsers(i, output)
                # Gather site information
                if len(self.json_obj['sites']) > 0:
                    site_count = len(self.json_obj['sites']) - 1
                    j = 0
                    # Launch i(th) site
                    while j <= site_count:
                        self.__run_sites(j, browser_objects['driver'], output)
                        # Pass i(th) data to ei
                        if len(self.json_obj['data']) > 0:
                            self.__run_data(browser_objects['ei'], output)
                        else:
                            raise Exception('No data too be tested')
                        j += 1
                else:
                    raise Exception('No sites too be tested')
                i += 1
                self.__report_step('Closed browser', output)
                self.driver.close()
        else:
            raise Exception('No browsers too be tested')
        self.__quit(start_time, output)

    def __run_browsers(self, counter, output):
        action = None
        # Not all drivers are tested, specifically mobile and apple
        if str(self.json_obj['browsers'][counter]['name']).lower() == 'chrome':
            self.driver = webdriver.Chrome(self.json_obj['browsers'][counter]['location'])
            action = 'Launched the Chrome browser'
        elif str(self.json_obj['browsers'][counter]['name']).lower() == 'opera':
            self.driver = webdriver.Opera(self.json_obj['browsers'][counter]['location'])
            action = 'Launched the Opera browser'
        elif str(self.json_obj['browsers'][counter]['name']).lower() == 'firefox':
            self.driver = webdriver.Firefox()
            action = 'Launched the Firefox browser'
        elif str(self.json_obj['browsers'][counter]['name']).lower() == 'android':
            self.driver = webdriver.Android(self.json_obj['browsers'][counter]['location'])
            action = 'Launched the Android web browser'
        elif str(self.json_obj['browsers'][counter]['name']).lower() == 'ios':
            self.driver = webdriver.Remote(self.json_obj['browsers'][counter]['location'])
            action = 'Launched the Safari mobile browser'
        elif str(self.json_obj['browsers'][counter]['name']).lower() == 'internet explorer':
            self.driver = webdriver.Ie(self.json_obj['browsers'][counter]['location'])
            action = 'Launched the Internet Explorer browser'
        elif str(self.json_obj['browsers'][counter]['name']).lower() == 'edge':
            self.driver = webdriver.Edge(self.json_obj['browsers'][counter]['location'])
            action = 'Launched the Edge browser'
        elif str(self.json_obj['browsers'][counter]['name']).lower() == 'safari':
            self.driver = webdriver.Safari(self.json_obj['browsers'][counter]['location'])
            action = 'Launched the Safari browser'
        else:
            self.__report_step((str(self.json_obj['browsers'][counter]['name']) + ' is not a supported browser'), output)
            raise Exception(str(self.json_obj['browsers'][counter]['name']) + ' is not a supported browser')
        self.__report_step(('\n' + action), output)
        self.driver.maximize_window()
        self.__report_step('Maximized the window', output)
        self.ei = ElementInteraction(self.driver)
        return {'driver': self.driver, 'ei': self.ei}

    def __run_sites(self, counter, driver, output):
        driver.get(self.json_obj['sites'][counter]['url'])
        if driver.name == 'MicrosoftEdge':
            time.sleep(3)
        self.__report_step(('Navigate to ' + self.json_obj['sites'][counter]['url']), output)

    def __run_data(self, ei, output):
        # Loop through steps
        action = None
        i = 0
        while i < len(self.json_obj['data']):
            for obj in self.json_obj['data']:
                if obj['order'] == i + 1:
                    results = self.__parse_data(str(obj['identifier']))
                    if obj['action'] == "click object":
                        action = ei.click_object(results)
                    elif obj['action'] == "enter text":
                        action = ei.enter_text(results, obj['text value'])
                    elif obj['action'] == "select option":
                        action = ei.select_option(results, obj['selection value'], obj['selection type'])
                    else:
                        raise Exception("Step " + obj['order'] + " does not have a known action type.")
            i += 1
            self.__report_step(action, output)

    def __create_output_file(self):
        options = self.json_obj['options']
        # Check for output directory
        if not os.path.exists(options['output location']):
            os.mkdir(options['output location'])
        if os.path.exists((options['output location'] + options['script name'] + '.txt')):
            os.remove((options['output location'] + options['script name'] + '.txt'))
        output = open((options['output location'] + options['script name'] + '.txt') , 'a+')
        return output

    def __report_step(self, action_to_report, output):
        output.write('\n' + action_to_report)

    def __email(self, email_address, email_subject, email_body, email_signature=None):
        # Determine if signature is required
        # Send email
        pass

    def __quit(self, start_time, output):
        email_address = self.json_obj['options']['email']
        stop_time = time.time()
        unix_runtime = stop_time - start_time
        runtime = datetime.datetime.fromtimestamp(unix_runtime).strftime('%Y-%m-%d %H:%M:%S')
        output.close()
        if email_address is not None:
            self.__email(email_address, self.json_obj['options']['script name'], ())
        self.driver.quit()
