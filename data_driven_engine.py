import json
import re
from element_interaction import ElementInteraction
from selenium import webdriver
import os
import time
import smtplib
from email.mime.text import MIMEText

class DataDrivenEngine(ElementInteraction):

    def __init__(self, name, path):
        self.script_name = name
        self.file_path = path
        file = open(self.file_path, 'r')
        raw_file_data = file.read()
        self.json_obj = json.loads(raw_file_data)

    def __parse_data(self, to_be_parsed):
        results = []

        tmp_list = list(to_be_parsed.items())
        dict_count = len(tmp_list)
        i = 0
        while i < dict_count:
            results.append(str(tmp_list[i][0]))
            results.append(str(tmp_list[i][1]))
            i += 1

        if results:
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
        self.__report_step(('Navigate to ' + self.json_obj['sites'][counter]['url']), output)

    def __run_data(self, ei, output):
        # Loop through steps
        action = None
        i = 0
        while i < len(self.json_obj['data']):
            for obj in self.json_obj['data']:
                if obj['order'] == i + 1: # Increase i by 1 to make json file human readable
                    results = self.__parse_data(obj['identifier'])
                    if obj['action'] == "click object":
                        action = ei.click_object(results, obj['child window'])
                    elif obj['action'] == "enter text":
                        action = ei.enter_text(results, obj['text value'], obj['child window'])
                    elif obj['action'] == "select option":
                        action = ei.select_option(results, obj['selection value'], obj['selection type'], obj['child window'])
                    elif obj['action'] == "handle alert":
                        action = ei.handle_alert(obj['alert action'], obj['child window'])
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

    def __email(self, email_address, email_subject, email_body, attachments=None, email_signature=None):
        ''' This function still needs code to handle attachments and an email signature'''

        message = MIMEText(email_body)
        message['Subject'] = email_subject
        message['From'] = 'zoebear@.com'
        match = re.search(".*?\w+@\w+\.\w+$",email_address)
        if match:
            message['To'] = email_address
        else:
            raise Exception('Email address is not valid')
        mail = smtplib.SMTP()
        mail.send_message(message)
        mail.quit()

    def __quit(self, start_time, output):
        email_address = self.json_obj['options']['email']
        stop_time = time.struct_time.tm_min
        unix_runtime = time.time() - start_time
        min, sec = divmod(unix_runtime, 60)
        hour, min = divmod(min, 60)
        runtime = '%d:%02d:%02d' % (hour, min, sec)
        output.write('\n\nTotal Runtime: ' + runtime)
        output.close()
        if email_address is not None:
            self.__email(email_address, self.json_obj['options']['script name'] + ' has completed.', self.json_obj['options']['script name'] + ' - Runtime: ' + runtime )
        self.driver.quit()
