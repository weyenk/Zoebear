import json
import re
from element_interaction import ElementInteraction
from selenium import webdriver


def parse_data(to_be_parsed):
    results = re.findall("'(\w+.*?)'", to_be_parsed)
    if results:
        # print(results)
        return results
    else:
        return None

file = open(r'/home/weyenk/Documents/big_cat_country_script', 'r')
raw_file_data = file.read()
json_obj = json.loads(raw_file_data)
i = 0
while i < len(json_obj['data']):
    for obj in json_obj['data']:
        if obj['order'] == i + 1:
            results = parse_data(str(obj['identifier']))
            if obj['action'] == "click object":
                pass
                # self.ei.click_object(results)
            elif obj['action'] == "enter text":
                pass
                # self.ei.enter_text(results, obj['text value'])
            elif obj['action'] == "select option":
                pass
                # self.ei.select_option(results, obj['selection value'], obj['selection type'])
            else:
                raise Exception("Step " + obj['order'] + " does not have a known action type.")
    i += 1


print(json_obj)
