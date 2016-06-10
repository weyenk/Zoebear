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

    def run_script(self):
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

        while 1 > 0:
            master_list = {}

            # Grab all tags and filter out all the tags we dont need
            tags = self.driver.find_elements_by_tag_name('a')
            tags.extend(self.driver.find_elements_by_tag_name('input'))
            tags.extend(self.driver.find_elements_by_tag_name('img'))
            tags.extend(self.driver.find_elements_by_tag_name('span'))
            tags.extend(self.driver.find_elements_by_tag_name('textbox'))
            tags.extend(self.driver.find_elements_by_tag_name('button'))
            tags.extend(self.driver.find_elements_by_tag_name('textarea'))
            tags.extend(self.driver.find_elements_by_tag_name('password'))
            tags.extend(self.driver.find_elements_by_tag_name('select'))
            tags.extend(self.driver.find_elements_by_tag_name('button'))

            start = time.perf_counter()
            id_list = self.__create_id_list(tags)
            href_list = self.__create_href_list(tags)
            name_list = self.__create_name_list(tags)
            src_list = self.__create_src_list(tags)
            alt_list = self.__create_alt_list(tags)
            title_list = self.__create_title_list(tags)
            text_list = self.__create_text_list(tags)
            value_list = self.__create_value_list(tags)
            class_list = self.__create_class_list(tags)
            print(time.perf_counter() - start)

            # Compare unordered data against the created dictionaries
            for obj in objs:
                for ident_item in obj['identifier'].items():
                    if ident_item[0] == 'id':
                        if ident_item[1] in id_list:
                            master_list[id_list.get(ident_item[1])] = obj
                    elif ident_item[0] == 'href':
                        if ident_item[1] in href_list:
                            master_list[href_list.get(ident_item[1])] = obj
                    elif ident_item[0] == 'name':
                        if ident_item[1] in name_list:
                            master_list[name_list.get(ident_item[1])] = obj
                    elif ident_item[0] == 'src':
                        if ident_item[1] in src_list:
                            master_list[src_list.get(ident_item[1])] = obj
                    elif ident_item[0] == 'alt':
                        if ident_item[1] in alt_list:
                            master_list[alt_list.get(ident_item[1])] = obj
                    elif ident_item[0] == 'title':
                        if ident_item[1] in title_list:
                            master_list[title_list.get(ident_item[1])] = obj
                    elif ident_item[0] == 'text()':
                        if ident_item[1] in text_list:
                            master_list[text_list.get(ident_item[1])] = obj
                    elif ident_item[0] == 'value':
                        if ident_item[1] in value_list:
                            master_list[value_list.get(ident_item[1])] = obj
                    elif ident_item[0] == 'class':
                        if ident_item[1] in class_list:
                            master_list[class_list.get(ident_item[1])] = obj

            # Sort keys from master list to determine order
            ordered_objs = []
            sorted_master = sorted(master_list.keys())
            for key in sorted_master:
                obj = master_list.get(key)
                ordered_objs.append(obj)

            self.__run_ordered_data(ordered_objs, ei, output)

    def __create_id_list(self, tags):
        id_list = {}
        i = 0
        for tag in tags:
            if not tag.get_attribute('type') == 'hidden':
                id_list[tag.get_attribute('id')] = i
                i += 1
        return id_list

    def __create_href_list(self,tags):
        href_list = {}
        i = 0
        for tag in tags:
            if not tag.get_attribute('type') == 'hidden':
                href_list[tag.get_attribute('herf')] = i
                i += 1
        return href_list

    def __create_name_list(self, tags):
        name_list = {}
        i = 0
        for tag in tags:
            if not tag.get_attribute('type') == 'hidden':
                name_list[tag.get_attribute('name')] = i
                i += 1
        return name_list

    def __create_src_list(self, tags):
        src_list = {}
        i = 0
        for tag in tags:
            if not tag.get_attribute('type') == 'hidden':
                src_list[tag.get_attribute('src')] = i
                i += 1
        return src_list

    def __create_alt_list(self, tags):
        alt_list = {}
        i = 0
        for tag in tags:
            if not tag.get_attribute('type') == 'hidden':
                alt_list[tag.get_attribute('alt')] = i
                i += 1
        return alt_list


    def __create_title_list(self, tags):
        title_list = {}
        i = 0
        for tag in tags:
            if not tag.get_attribute('type') == 'hidden':
                title_list[tag.get_attribute('title')] = i
                i += 1
        return title_list

    def __create_text_list(self, tags):
        text_list = {}
        i = 0
        for tag in tags:
            if not tag.get_attribute('type') == 'hidden':
                text_list[tag.get_attribute('innerText')] = i
                i += 1
        return text_list

    def __create_value_list(self, tags):
        value_list = {}
        i = 0
        for tag in tags:
            if not tag.get_attribute('type') == 'hidden':
                value_list[tag.get_attribute('value')] = i
                i += 1
        return value_list

    def __create_class_list(self, tags):
        class_list = {}
        i = 0
        for tag in tags:
            if not tag.get_attribute('type') == 'hidden':
                class_list[tag.get_attribute('class')] = i
                i += 1
        return class_list

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
