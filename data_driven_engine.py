from element_interaction import ElementInteraction
from email.mime.text import MIMEText
from selenium import webdriver
import smtplib
import json
import time
import re
import os


class DataDrivenEngine(ElementInteraction):

    def __init__(self, name, path):

        # Open path/element script
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

    def run_ordered_script(self):
        start_time = time.time()

        # Create output file
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
                            k = 0
                            while k <= len(self.json_obj['data']) - 1:
                                ordered = None
                                unordered = None
                                try:
                                    ordered = self.json_obj['data'][k]['ordered']
                                except:
                                    pass
                                try:
                                    unordered = self.json_obj['data'][k]['unordered']
                                except:
                                    pass
                                #test = get_child_nodes(self.json_obj['data'][k])
                                if ordered is not None:
                                    self.__run_ordered_data(self.json_obj['data'][k]['ordered'], browser_objects['ei'], output)
                                elif unordered is not None:
                                    self.__run_unordered_data(self.json_obj['data'][k]['unordered'], browser_objects['ei'], output)
                                else:
                                    raise Exception('Unknown data structure')
                                k += 1
                        else:
                            raise Exception('No data too be tested')
                        j += 1
                else:
                    raise Exception('No sites too be tested')
                i += 1

                # Close browser and report actions
                self.__report_step('Closed browser', output)
                self.driver.close()
        else:
            raise Exception('No browsers too be tested')

        # Finalize script
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

        # Report browser launch and maximization
        self.__report_step(('\n' + action), output)
        self.driver.maximize_window()
        self.__report_step('Maximized the window', output)

        # Create ei object
        self.ei = ElementInteraction(self.driver)

        return {'driver': self.driver, 'ei': self.ei}

    def __run_sites(self, counter, driver, output):
        driver.get(self.json_obj['sites'][counter]['url'])
        self.__report_step(('Navigate to ' + self.json_obj['sites'][counter]['url']), output)

    def __run_ordered_data(self,objs, ei, output):
        action = None

        for obj in objs:
            if obj['action'] == "click object":
                action = ei.click_object(obj)
            elif obj['action'] == "enter text":
                action = ei.enter_text(obj)
            elif obj['action'] == "select option":
                action = ei.select_option(obj)
            elif obj['action'] == "handle alert":
                action = ei.handle_alert(obj)
            else:
                raise Exception("Unknown action type.")

        self.__report_step(action, output)

    def __run_unordered_data(self, objs, ei, output):
        id_list = {}
        href_list = {}
        name_list = {}
        src_list = {}
        alt_list = {}
        title_list = {}
        text_list = {}
        i = 0
        # Grab all tags and filter out all the tags we dont need
        tags = self.driver.find_elements_by_tag_name('*')
        for tag in tags:
            if tag.tag_name == 'input' or tag.tag_name == 'a' or tag.tag_name == 'img' or tag.tag_name == 'span' or tag.tag_name == 'textbox' or tag.tag_name == 'button' or tag.tag_name == 'textarea' or tag.tag_name == 'password':
                if not tag.get_attribute('type') == 'hidden':
                    if tag.get_attribute('id') is not None or not tag.get_attribute('id') == '':
                        id_list[tag.get_attribute('id')] = i
                        if tag.get_attribute('herf') is not None or not tag.get_attribute('href') == '':
                            href_list[tag.get_attribute('herf')] = i
                        if tag.get_attribute('name') is not None or not tag.get_attribute('name') == '':
                            name_list[tag.get_attribute('name')] = i
                        if tag.get_attribute('src') is not None or not tag.get_attribute('src') == '':
                            src_list[tag.get_attribute('src')] = i
                        if tag.get_attribute('alt') is not None or not tag.get_attribute('alt') == '':
                            alt_list[tag.get_attribute('alt')] = i
                        if tag.get_attribute('title') is not None or not tag.get_attribute('title') == '':
                            title_list[tag.get_attribute('title')] = i
                        if tag.get_attribute('innerText') is not None or not tag.get_attribute('innerText') == '':
                            text_list[tag.get_attribute('innerText')] = i
                        i += 1


        ''' From here I would like to loop over the unordered list.  Any matches should be put in a dictionary where the
            key is the i number and the identifiers are the values. The dictionary will then provide the order in which
            the unordered list elements are fed into element_interaction'''

        for obj in objs:
            if not page_html == self.driver.page_source:
                page_html = self.driver.page_source
                continue
            for ident_item in obj['identifier'].items():
                if tag.get_attribute(ident_item[0]) == ident_item[1]:
                    if obj['action'] == "click object":
                        action = ei.click_object(obj)
                    elif obj['action'] == "enter text":
                        action = ei.enter_text(obj)
                    elif obj['action'] == "select option":
                        action = ei.select_option(obj)
                    elif obj['action'] == "handle alert":
                        action = ei.handle_alert(obj)
                    else:
                        raise Exception("Unknown action type.")
                    self.__report_step(action, output)
        print('test')

    def __create_output_file(self):
        options = self.json_obj['options']

        # Check for output directory
        if not os.path.exists(options['output_location']):
            os.mkdir(options['output_location'])
        if os.path.exists((options['output_location'] + options['script name'] + '.txt')):
            os.remove((options['output_location'] + options['script name'] + '.txt'))

        # Create and open output file
        output = open((options['output_location'] + options['script name'] + '.txt'), 'a+')
        return output

    def __report_step(self, action_to_report, output):
        output.write('\n' + action_to_report)

    def __email(self, email_address, email_subject, email_body, attachments=None, email_signature=None):
        ''' This function still needs code to handle attachments and an email signature'''

        # Build message
        message = MIMEText(email_body)
        message['Subject'] = email_subject
        message['From'] = ''

        # Validate email address
        match = re.search(".*?\w+@\w+\.\w+$",email_address)
        if match:
            message['To'] = email_address
        else:
            raise Exception('Email address is not valid')
        mail = smtplib.SMTP('')

        # Send completed message
        mail.send_message(message)
        mail.quit()

    def __quit(self, start_time, output):
        email_address = self.json_obj['options']['email']
        unix_runtime = time.time() - start_time

        # Format time in a human readable format
        min, sec = divmod(unix_runtime, 60)
        hour, min = divmod(min, 60)
        runtime = '%d:%02d:%02d' % (hour, min, sec)

        # Output runtime and close file
        output.write('\n\nTotal Runtime: ' + runtime)
        output.close()

        # Email results to analyst if email is provided
        if email_address is not None:
            self.__email(email_address, self.json_obj['options']['script name'] + ' has completed.', self.json_obj['options']['script name'] + ' - Runtime: ' + runtime )
        self.driver.quit()
